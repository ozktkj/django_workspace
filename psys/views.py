from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from functools import wraps
from .forms import CustomerSearchForm,LoginForm
from .models import Customer,Employee

# ログインチェック関数
def employee_auth_required(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        if not request.session.get("employee_no"):
            return redirect("psys:login")
        return view_func(request,*args,**kwargs)
    return wrapper

def index(request):
    return render(request,"psys/index.html")

@employee_auth_required
def MainMenu(request):
    return render(request,"psys/MainMenu.html")

@employee_auth_required
def CustomerManagementMenu(request):
    return render(request, "psys/CustomerManagementMenu.html")

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            employee_no = form.cleaned_data['employee_no']
            password = form.cleaned_data['password']

            login_failed = False
            try:
                # 従業員番号でレコードを検索
                employee = Employee.objects.get(employee_no=employee_no)
                
                # パスワードの比較
                if employee.password != password:
                    login_failed = True
                else:
                    # ログイン成功
                    request.session['employee_no'] = employee.employee_no
                    request.session['employee_name'] = employee.employee_name
                    return redirect('psys:main_menu')
                    
            except Employee.DoesNotExist:
                # ユーザーが存在しない場合もフラグを立てる
                login_failed = True

            if login_failed:
                # PRGパターン: エラー文言をセッションに格納してGETリクエストへ飛ばす
                request.session['login_error'] = "従業員番号、またはパスワードに誤りがあります。"
                return redirect('psys:login')
        else:
            # フォーム自体のバリデーションがFalse
            request.session['login_error'] = "従業員番号、またはパスワードに誤りがあります。"
            return redirect('psys:login')

    else:
        # GETリクエスト時：セッションからエラーメッセージを取り出して1回だけ表示（ポップ）
        form = LoginForm()
        error_message = request.session.pop('login_error', None)
        
        context = {
            'form': form,
            'error_message': error_message
        }
        return render(request, 'psys/login.html', context)

@employee_auth_required
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
        # バリデーションエラー
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

# 確認用簡易ログアウト
def logout(request):
    request.session.flush()
    return redirect("psys:login")