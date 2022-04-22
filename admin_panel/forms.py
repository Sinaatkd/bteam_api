from django import forms

class EditUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}))
    national_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد ملی'}))
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}))
    from_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'}))
    is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}), label='ادمین بودن/نبودن', required=False)
    wallet = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'موجودی کیف پول'}))
