from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .forms import CustomerSearchForm
from .models import Customer

def CustomerSearch(request):
    customer = None
    error_message = None
    form = CustomerSearchForm()
    if request.method == 'POST':

        # バリデーション
        form = CustomerSearchForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get("customer_code")
            #sessionにseartch_idを格納
            request.session["seartch_customer_code"] = code
            #redirect
            return redirect('psys:CustomerSearch')    
        else:
            errors = form.errors.get('customer_code')
            if errors:
                error_message = errors[0]    
    else:
        # セッションから顧客IDを取得
        code = request.session.pop("seartch_customer_code",None)

        if code:
            form = CustomerSearchForm(initial={'customer_code':code})
            try:
                customer = Customer.objects.get(customer_code=code)
            except ObjectDoesNotExist:
                error_message = "該当する顧客は登録されていません"

    context = {
        'form':form,
        'customer':customer,
        'error_message':error_message
    }
        
    return render(request,"psys/CustomerSearch.html",context)