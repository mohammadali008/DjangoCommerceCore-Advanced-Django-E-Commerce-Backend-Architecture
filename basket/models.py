from django.contrib.auth.models import User
from django.db import models

from catalogue.models import Product


# Create your models here.
class Basket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='baskets',blank=True,null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"
    # --- Define Add function --- #
    def add(self,product,product_quantity):
        product_line = self.lines.filter(product = product)
        if product_line.exists():
            product_line = product_line.first()
            if product_quantity is not None:
                product_line.quantity += int(product_quantity)
                product_line.save()
            else:
                product_line.quantity += 1
                product_line.save()
        else:
            product_line = self.lines.create(
                product = product ,
                quantity= int(product_quantity)
            )
            return product_line
    # --- Define ValidateUser --- #
    def validate_user(self,user):
        pass


# --- Define BasketLine to keep our product with Its quantity in basket --- #
class BasketLine(models.Model):

    basket = models.ForeignKey(Basket,on_delete=models.CASCADE,related_name='lines')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='lines')
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.basket} = {self.product},{self.quantity}"

