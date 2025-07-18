from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')
    city = models.CharField(max_length=32,blank=True)
    zipcode = models.CharField(max_length=16)
    address = models.CharField(blank=True)
    number = models.PositiveSmallIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    # --- Define Main Methods --- #
    def __str__(self):
        return str(self.user)
    # Todo: Define suitable validation for Model-Fields


