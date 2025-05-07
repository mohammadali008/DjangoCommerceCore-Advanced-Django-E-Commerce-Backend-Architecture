from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from shipping.forms import ShippingAddressForm
from shipping.models import ShippingAddress


# Create your views here.
# --- Define AddressList --- #
def AddressList(request):
    pass

# --- Define ClassBaseView of AddressList --- #
class AddressListView(View):
    @method_decorator(login_required)
    def get(self,request):
        queryset = ShippingAddress.objects.filte(user = request.user)
        return render(request,'shipping/list.html',{'items':queryset})
class AddressListView(ListView):
    model = ShippingAddress
    # --- OverWrite dispatch method --- #
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # -- overwrite get_queryset methode --- #
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.first(user = self.request.user)
# --- Define CreateAddress --- #
@login_required
@require_http_methods(request_method_list=['GET','POST'])
def CreateAddress(request):
    if request.method == 'POST':
        # Todo: Validate a form and save data
        print('post')
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            print('valid')
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            return redirect('/')
    else:
        form = ShippingAddressForm()
    return render(request, 'shipping/create.html', {'form': form})


