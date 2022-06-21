from django.shortcuts import redirect

from django.views.generic import ListView
from admin_panel.decorators import check_group
from utilities import send_notification
from news.models import News

class NewsList(ListView):
    queryset = News.objects.all().order_by('-id')
    template_name = 'news/news_list.html'
    paginate_by = 20


@check_group('دسترسی به اخبار')
def delete_news(request, news_id):
    news = News.objects.get(id=news_id)
    news.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@check_group('دسترسی به اخبار')
def add_new(request):
    if request.method == 'POST':
        news_img = request.FILES.get('news_img')
        title = request.POST.get('title')
        short_description = request.POST.get('short_description')
        description = request.POST.get('description')
        News.objects.create(title=title, short_description=short_description, description=description, img=news_img)
        send_notification('بی‌تیم نیوز!', short_description, False)

    return redirect(request.META.get('HTTP_REFERER'))
