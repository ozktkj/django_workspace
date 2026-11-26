from django.db import IntegrityError, transaction
from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from functools import wraps
from .forms import CustomerSearchForm,LoginForm,CustomerRegistForm
from .models import Customer,Employee,CustomerNumbering

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

@employee_auth_required
def CustomerRegist(request):
    if request.method == 'POST':
        form = CustomerRegistForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():#トランザクション処理
                    # 採番テーブルから最新番号を取得
                    seq = CustomerNumbering.objects.select_for_update().get()
                    next_num = seq.customer_code + 1
                    next_code = f"RA{next_num:04d}"

                    # 採番テーブルを更新(主キーがないため再検索してアップデート)
                    CustomerNumbering.objects.filter(
                        customer_code=seq.customer_code
                    ).update(customer_code=next_num)

                    # 得意先に追加
                    customer = form.save(commit=False) #得意先を生成(コミットしない)
                    customer.customer_code = next_code #得意先番号を設定
                    customer.delete_flag = 0 #論理削除をFalse
                    customer.discount_rate = 0 #割引率をゼロ
                    customer.save(force_insert=True) #INSERTを強制
                    form.save_m2m() #commit=Falseの解消
                    return redirect('psys:CustomerRegistDone')

            except IntegrityError as e:# DB整合性エラー
                form.add_error(None, f"登録処理でエラーが発生: {e}")
    else:
        form = CustomerRegistForm()
    context = {
        "form":form,
        "title":"Regist",
        }
    return render(request,"psys/CustomerRegist.html",context)

# 仕様にはないがPRGパターンのための完了画面
@employee_auth_required
def CustomerRegistDone(request):
    return render(request,'psys/CustomerRegistDone.html')