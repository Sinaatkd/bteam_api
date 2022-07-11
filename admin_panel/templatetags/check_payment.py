from django import template
# from django.contrib.auth.models import Permission

register = template.Library()

@register.filter(name='user_is_payer') 
def user_is_payer(user, basket):
    last_pay_time_stage = basket.stages.filter(is_pay_time=True, payers__in=[user]).last()
    return last_pay_time_stage is not None