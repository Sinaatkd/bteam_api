from django.db import models

from base_model.models import BaseModel

from utilities import get_filename_ext

def new_upload_img_path(instance, filepath):
    name, ext = get_filename_ext(filepath)
    new_name = f'{instance.title}'
    path = f'news/{instance.title}/{new_name}{ext}'
    return path


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.title

class News(BaseModel):
    title = models.CharField(max_length=3000)
    short_description = models.CharField(max_length=5000)
    description = models.TextField()
    img = models.ImageField(upload_to=new_upload_img_path, null=True, blank=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
