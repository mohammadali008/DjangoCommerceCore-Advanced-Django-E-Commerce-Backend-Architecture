from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce


# Create your models here.
## Define Transaction Table
class Transaction(models.Model):
    CHARGE = 1
    PURCHASE = 2
    TRANSFER_RECEIVED = 3
    TRANSFER_sent = 4

    TRANSACTION_TYPE_CHOICES = (
        (CHARGE,'شارژ'),
        (PURCHASE,'برداشت'),
        (TRANSFER_RECEIVED,'دیافت'),
        (TRANSFER_sent,'انتقال'),
    )
    ###
    user = models.ForeignKey(User,on_delete=models.RESTRICT,related_name='transactions')
    transaction_type = models.PositiveSmallIntegerField(default=CHARGE,choices=TRANSACTION_TYPE_CHOICES)
    amount = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    ### Define main method ###
    def __str__(self):
        return f"{self.user}-{self.get_transaction_type_display()}-{self.amount}"
    @classmethod
    def get_report(cls):
        """Show all users with their transactions"""
        positive_transactions = Sum('transactions__amount',filter=Q(transactions__transaction_type=1))
        negative_transactions = Sum('transactions__amount',filter=Q(transactions__transaction_type__in=[2,3]))
        users = User.objects.all().annotate(
            transaction_count = Count('transactions__id'),
            balance=(Coalesce(positive_transactions,0)-Coalesce(negative_transactions,0)),
        )
        print(curses)
        return users

    @classmethod
    def get_total_balance(cls):
        # current_user = User.objects.all().aggregate(
        #     Count('transactions__id')
        # )
        # print(current_user)
        # return current_user
        #--- annotate & aggregate
        queryset = cls.get_report()
        print(queryset.aggregate(Sum('balance')))
        return queryset.aggregate(Sum('balance'))
    @classmethod
    def user_balance(cls,user):
        positive_transactions = Sum('amount', filter=Q(transaction_type__in=[1,3]))
        negative_transactions = Sum('amount', filter=Q(transaction_type__in=[2, 4]))

        current_user_balance = user.transactions.all().aggregate(
            balance=(Coalesce(positive_transactions, 0) - (Coalesce(negative_transactions, 0)))
        )
        return current_user_balance


### Define UserBalance Table ###
class UserBalance(models.Model):
    user = models.ForeignKey(User,on_delete=models.RESTRICT,related_name='balance_records')
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    #---Define main Methodes ---#
    def __str__(self):
        return f"{self.user}-{self.balance}-{self.created_time}"
    ### Define Main methods ###
    @classmethod
    def record_user_balance(cls,user):
        balance = Transaction.User_balance(user)
        instance = cls.objects.create(
            user = user,balance=balance['balance']
        )
        print(instance)
        return instance
    @classmethod
    def record_all_user_balance(cls):
        queryset = User.objects.all()
        for user in queryset:
            record=cls.record_user_balance(user)
            print(record)


###---Define TransactionArchive --- #

### --- TransferTransaction --- ###
class TransferTransaction(models.Model):
    # It's better to user OnetToOne relation insted of ForeignKey in sender and receiver
    sender_transaction = models.ForeignKey(Transaction,on_delete=models.RESTRICT,related_name = 'sent_transactions')
    receiver_transaction = models.ForeignKey(Transaction,on_delete=models.RESTRICT,related_name = 'received_transactions')

    def __str__(self):
        return f"{self.sender_transaction} >>> {self.receiver_transaction}"
    #---Define Main ClassMethod ---#
    @classmethod
    def transfer(cls,sender,receiver,amount):
        if (Transaction.user_balance(sender)) < amount:
            return "The transaction not allowed!  insufficient balance"
        with transaction.atomic():
            sender_transaction = Transaction.objects.create(
                user=sender, amount=amount, transaction_type=Transaction.TRANSFER_sents
            )
            receiver_transaction = Transaction.objects.create(
                user=receiver, amount=amount, transaction_type=Transaction.TRANSFER_RECEIVED
            )
            instance = cls.objects.create(
                sender_transaction = sender_transaction,
                receiver_transaction = receiver_transaction
            )
        return instance


### --- Define UserScore Table --- ###
class UserScore(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.user}-{self.score}"
    #--- Define Main Method ---#
    def charge_score(self,user,score):
        with transaction.atomic():
            instance = cls.objects.select_for_update().filter(user = user)
            if not instance.exists():
                instance = cls.objects.create(user = user,score = 0)
            else:
                instance.first()
            instance.score += score
            instance.save()


        # try:
        #     instance = cls.objects.get(user=user)
        # except User.DoesNotExist:
        #     instance = cls.objects.create(
        #         user = user,score = 0
        #     )
        # instance.score += score
        # instance.save()











