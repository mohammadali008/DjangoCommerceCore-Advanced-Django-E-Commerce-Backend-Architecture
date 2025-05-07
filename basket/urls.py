from django.urls import path
from .views import *

# --- Define root of basket app ---#
urlpatterns = [
    path('add/',AddToBasket,name='add_to_basket'),
]