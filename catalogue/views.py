from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.shortcuts import render

from basket.form import AddToBasketForm
from .models import *
from django.http import HttpResponse, Http404

from .utils import check_is_active


# Create your views here.
### Define ProductList view ###
def ProductList(request):
    # products = Product.objects.all()
    # context = [f"{product.title}{product.upc}" for product in products]
    category = Category.objects.last()
    # products = Product.objects.filter(category = category)
    # products = Product.objects.filter(category__name= 'school')
    # context = [f"{product.title}{product.upc}" for product in products]
    # return HttpResponse(context)
    # return HttpResponse('This is List of all Products')
    context = dict()
    context['products'] = Product.objects.select_related('category').all()
    print(context)
    # print(Product.objects.select_related('category').images.all())
    return render(request,'catalogue/product_list.html',context = context)

### Define ProductDetail view
def ProductDetail(request,pk):
    # try:
    #     product = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     return HttpResponse('The product that you chose is not exist !!! ')
    # context = Product.objects.filter(Q(pk=pk)|Q(upc=pk))
    # return HttpResponse(context)
    product_query = Product.default_objects.filter(Q(pk=pk)|Q(upc=pk))
    if product_query.exists():
        product = product_query.first()
        add_form = AddToBasketForm(
            {'product':product.id}
        )
        context = dict()
        context['product'] = product_query
        context['form'] = add_form
        return render(request, 'catalogue/product_detail.html', context=context)
    else:
        raise Http404





###Define ProductCategory view
def ProductCategory(request,pk):
    # method 1 #
    # try:
    #     queryset = Category.objects.get(pk=pk)
    # except Category.DoesNotExist:
    #     return HttpResponse("The category that you chose is not exist !!!")
    # # products = Product.objects.filter(category=catalogue)
    # products = queryset.products.all()
    # methode 2 #
    try:
        category = Category.objects.prefetch_related('products').get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse('The category witch you chose is not exist !!!')
    products = category.products.all()
    return HttpResponse(products)

# --- Define ProductSearchView --- #
def ProductSearchView(request):
    # title = request.GET['q']
    title = request.GET.get('q')
    products = Product.objects.filter(title=title)
    context = [f"{product.title}-{product.upc}" for product in products]
    print(products)
    print(context)
    return HttpResponse(f"Your result of search : {context}")

# --- Define views with login required ---#
@login_required(login_url='/admin/login/')
@require_http_methods(request_method_list=['GET'])
@user_passes_test(check_is_active)
# @permission_required('transaction.has_score_permission')
def UserProfile(request):
    return HttpResponse(f"Hellow {request.user.username}")




