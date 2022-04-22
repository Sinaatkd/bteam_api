import jdatetime
from django.db import models
from account.models import User
from base_model.models import IntegerRangeField
from special_account_item.models import SpecialAccountItem

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    validity_date = models.DateTimeField()
    percentage = IntegerRangeField(min_value=0, max_value=100)
    create_date = models.DateTimeField(auto_now_add=True)
    use_by = models.ManyToManyField(User, blank=True)
    count = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.code

    def jalali_validaty_date(self):
        jdate = jdatetime.GregorianToJalali(self.validity_date.year, self.validity_date.month, self.validity_date.day).getJalaliList()
        jdate = '{year}/{month}/{day}'.format(year=jdate[2], month=jdate[1], day=jdate[0])
        return jdate

class Transaction(models.Model):
    payment_mode = models.CharField(max_length=20, choices=(('online', 'آنلاین'), ('offline', 'کارت به کارت')))
    amount = models.FloatField()
    special_item = models.ForeignKey(SpecialAccountItem, on_delete=models.CASCADE, null=True, blank=True)
    date_of_approval = models.DateTimeField(null=True, blank=True)
    last_updated_time = models.DateTimeField(auto_now_add=True)
    validity_rate = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, null=True, blank=True)
    transaction_status = models.CharField(max_length=300, null=True, blank=True)
    is_confirmation = models.BooleanField(default=False)
    consultant_name = models.CharField(max_length=300, null=True, blank=True)
    payment_receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    is_send_receipt = models.BooleanField(default=False)
    


    def __str__(self) -> str:
        return f'{self.user.full_name} -- {self.amount}'
