from django import template
# from django.contrib.auth.models import Permission

register = template.Library()

@register.filter(name='user_is_payer') 
def user_is_payer(user, basket):
    print(basket)
    print(user)
    last_pay_time_stage = basket.stages.filter(is_pay_time=True, payers__in=[user]).last()
    print(last_pay_time_stage)
    return last_pay_time_stage is not None