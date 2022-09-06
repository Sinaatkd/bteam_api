# Generated by Django 4.0.4 on 2022-09-06 15:18

from django.db import migrations, models
import news.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_category_news_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=200, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='news',
            name='categories',
            field=models.ManyToManyField(to='news.category', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='news',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=news.models.new_upload_img_path, verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='news',
            name='short_description',
            field=models.CharField(max_length=5000, verbose_name='توضیحات کوتاه'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=3000, verbose_name='عنوان'),
        ),
    ]
