from django import forms

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