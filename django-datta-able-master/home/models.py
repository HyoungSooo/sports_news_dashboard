from django.db import models
from datetime import datetime
# Create your models here.

class DefaultDate(models.Model):
    date = models.DateField(default= datetime.now().date().strftime("%Y-%m-%d"))
    sync = models.BooleanField(default=False)
    crawl = models.BooleanField(default=False)

class Product(models.Model):
    date = models.ForeignKey(DefaultDate, on_delete=models.CASCADE, related_name='news')
    title = models.TextField()
    content = models.TextField()
    url = models.URLField()
    office = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField()
    category = models.CharField(max_length=20)

class WordCloud(models.Model):
    date = models.ForeignKey(DefaultDate, on_delete=models.CASCADE, related_name='words')
    string = models.TextField()
    count = models.IntegerField()
    category = models.CharField(max_length=20)
