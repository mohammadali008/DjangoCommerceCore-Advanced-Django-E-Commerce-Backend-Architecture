from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__','created_time']


### Register as Inline methode ###
# admin.site.register(Transaction)
admin.site.register(UserBalance)