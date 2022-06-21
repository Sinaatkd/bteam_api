from django.db import models


class Banner(models.Model):
    img = models.ImageField(upload_to='banners/')
    link = models.URLField()

    def __str__(self):
        return self.link