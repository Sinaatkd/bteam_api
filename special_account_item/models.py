from django.db import models
from base_model.models import BaseModel

# Create your models here.
class SpecialAccountItem(BaseModel):
    title = models.CharField(max_length=250)
    price = models.PositiveBigIntegerField(default=0)
    expire_day = models.PositiveIntegerField()

    def __str__(self):
        return self.title
