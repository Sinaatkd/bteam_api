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
    title = models.CharField(verbose_name='عنوان', max_length=3000)
    short_description = models.CharField(verbose_name='توضیحات کوتاه', max_length=5000)
    description = models.TextField(verbose_name='توضیحات')
    img = models.ImageField(verbose_name='تصویر', upload_to=new_upload_img_path, null=True, blank=True)
    categories = models.ManyToManyField(Category, verbose_name='دسته بندی')

    def __str__(self):
        return self.title
