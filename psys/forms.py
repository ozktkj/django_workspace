from django import forms
from .models import Employee

# 得意先検索フォーム
class CustomerSearchForm(forms.Form):
    customer_code = forms.CharField(
        required=True,
        max_length=6,
        label="顧客コード",
        widget=forms.TextInput(attrs={
            'placeholder':'123456',
            'maxlength':'6',
            'class':'search-input'
        })
    )

    def clean_customer_code(self):
        code = self.cleaned_data.get('customer_code')
        if not code:
            raise forms.ValidationError("顧客コードを入力してください")
        return code

# ログインンフォーム
class LoginForm(forms.Form):
    employee_no = forms.CharField(
        label="従業員番号",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )