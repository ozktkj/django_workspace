# テンプレート用ログイン確認関数
# settings.pyに登録する
def employee_auth(request):
    return {
        "employee_no":request.session.get('employee_no'),
        "employee_name":request.session.get('employee_name'),
    }