from django.urls import path
from .views import *
# --- #
urlpatterns = [
    path('list/',AddressList,name = 'address_list'),
    path('create/',CreateAddress,name='create_address')
]