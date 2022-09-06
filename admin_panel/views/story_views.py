from django.views.generic import ListView, CreateView
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from admin_panel.forms import StoryForm
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

class CreateStory(CreateView):
    model = Story
    form_class = StoryForm


    def form_valid(self, form):        
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse('stories_list'))


def delete_story(request, pk):
    selected_story = Story.objects.get(pk=pk)
    selected_story.delete()
    return HttpResponseRedirect(reverse('stories_list'))