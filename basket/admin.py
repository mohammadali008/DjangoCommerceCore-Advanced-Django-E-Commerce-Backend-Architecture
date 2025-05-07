from django.contrib import admin
from .models import *

# Register your models here.
# Define BasketLine model as InLIne model
class BasketLineInline(admin.TabularInline):
    model = BasketLine

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    inlines = (BasketLineInline,)