from django.views.generic import ListView
from django.http import Http404, HttpResponseRedirect

from story.models import Story

class StoryList(ListView):
    model = Story
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='استوری').exists() or request.user.groups.filter(name='مدیر').exists():
            return super().dispatch(request, *args, **kwargs)
        raise Http404

    def get_queryset(self):
        if self.request.user.groups.filter(name='مدیر').exists():
            return Story.objects.all().order_by('-id')
        return Story.objects.filter(user=self.request.user).order_by('-id')