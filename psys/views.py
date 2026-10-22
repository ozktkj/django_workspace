from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Customer

def CustomerSearch(request):
    if request.method == 'POST':

        # バリデーション

        seartch_id = request.POST.get('seartch_id')
        result = Customer.objects.get(pk=seartch_id)
        #sessionにseartch_idを格納
        request.session["seartch_result"] = {
            'seartch_id':seartch_id,
            'customer_name':result.customer_name,
            'customer_telno':result.customer_telno,
            'customer_postalcode':result.customer_postalcode,
            'customer_address':result.customer_address,
        }
        

        return redirect('psys:CustomerSearch')
        
    else:
        context = {"seartch_id":None}
        if request.session.get('seartch_result', False):
            context = request.session['seartch_result']
            # 取得したら削除
            del request.session['seartch_result']
            print(context)
            
        return render(request,"psys/CustomerSearch.html",context)