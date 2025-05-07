from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.decorators.http import require_POST

from basket.form import AddToBasketForm
from basket.models import Basket
from catalogue.models import Product


# Create your views here.
# --- Define AddToBasket function base view --- #

def AddToBasket(request):
    # todo-1: check user hase basket_id in cookie .
    # todo 2: create basket if user doesn't have basket
    # todo 2-1: check authentication of user
    # todo 3: get product from submitted form
    # todo 4: add product to the user basket line
    # todo 5: return user to next url
    response = HttpResponseRedirect(request.POST.get('next','/'))
    basket_id = request.COOKIES.get('basket_id',None)
    # - step:1
    if basket_id is None:
        basket = Basket.objects.create()
        response.set_cookie('basket_id',basket.id)
    else:
        try:
            basket = Basket.objects.get(pk= basket_id)
        except Basket.DoesNotExist:
            print('does not exist')
            raise Http404
        # -step: 2-1
        if request.user.is_authenticated:
            if basket.user is not None and basket.user != request.user:
                raise Http404
            basket.user = request.user
            basket.save()
    # -step:3 -- method :1
    # product_id = request.POST.get('product_id',None)
    # product_quantity = request.POST.get('quantity',None)
    # if product_id is not None:
    #     try:
    #         product = Product.default_objects.get(pk = product_id)
    #     except Product.DoesNotExist:
    #         print("Product not existed !")
    #         raise Http404
    #     else:
    #         basket.add(product,product_quantity)
    # -step:3 -- method :2
    add_form = AddToBasketForm(request.POST)
    if add_form.is_valid():
        add_form.save(basket = basket)
    print(request)
    return response
    # return HttpResponse('ok')