from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Link(models.Model):
    url = models.CharField('Link Url', max_length=200)
    store = models.CharField('Store', max_length=50)
    threshold = models.CharField(max_length=10)
    active = models.CharField('Active (True/False)', max_length=6, default='True')
    title = models.CharField('Product name', max_length=100, default='Product Name')
    owner = models.ForeignKey(User, default=None, on_delete=models.PROTECT)

    def __str__(self):
        return self.url