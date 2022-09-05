from django import forms

from copy_trade.models import Basket, Stage
from news.models import Category, News

class EditUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}))
    national_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد ملی'}))
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}))
    from_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'}))
    is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}), label='ادمین بودن/نبودن', required=False)
    wallet = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'موجودی کیف پول'}))


class BasketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Basket
        exclude = ('trader','exchange','participants','blocked_users','is_freeze','is_accept_participant','is_active','orders_count', 'stages', 'orders')


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        exclude = ('payers', 'pay_datetime', 'is_pay_time')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})
    

class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = News
        exclude = ('is_active',)

    

class NewsCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Category
        fields = '__all__'
