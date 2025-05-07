from django.urls import path
from .views import *

### Define uour urls ###
urlpatterns = [
    path('product/list/',ProductList,name = 'product_list'),
    path('product/detail/<int:pk>/',ProductDetail,name = 'product_detail'),
    path('product/<int:pk>/',ProductCategory,name = 'product_category'),
    path('product/search/',ProductSearchView,name = 'product_search_view'),
    path('user_profile/',UserProfile,name = 'user_profile'),

]