from django.shortcuts import redirect
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy

from admin_panel.decorators import check_group
from admin_panel.forms import NewsCategoryForm, NewsForm
from utilities import send_notification
from news.models import Category, News

class NewsList(ListView):
    queryset = News.objects.all().order_by('-id')
    template_name = 'news/news_list.html'
    paginate_by = 20


class CreateNews(CreateView):
    model = News
    form_class = NewsForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='دسترسی به اخبار').exists() or request.user.groups.filter(name='مدیر').exists():
            return super().dispatch(request, *args, **kwargs)
        raise Http404


    def form_valid(self, form):
        obj = form.save()
        send_notification('بی‌تیم نیوز!', obj.short_description, False)
        return HttpResponseRedirect(reverse('news_list'))


class UpdateNews(UpdateView):
    model = News
    form_class = NewsForm
    success_url = reverse_lazy('news_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='دسترسی به اخبار').exists() or request.user.groups.filter(name='مدیر').exists():
            return super().dispatch(request, *args, **kwargs)
        raise Http404


@check_group('دسترسی به اخبار')
def delete_news(request, news_id):
    news = News.objects.get(id=news_id)
    news.delete()
    return redirect(request.META.get('HTTP_REFERER'))



class NewsCategoriesList(ListView):
    queryset = Category.objects.all().order_by('-id')
    template_name = 'news/categories_list.html'
    paginate_by = 20


class CreateNewsCategory(CreateView):
    model = Category
    form_class = NewsCategoryForm
    success_url = reverse_lazy('news_categories_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='دسترسی به اخبار').exists() or request.user.groups.filter(name='مدیر').exists():
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class UpdateNewsCategory(UpdateView):
    model = Category
    form_class = NewsForm
    success_url = reverse_lazy('news_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='دسترسی به اخبار').exists() or request.user.groups.filter(name='مدیر').exists():
            return super().dispatch(request, *args, **kwargs)
        raise Http404

