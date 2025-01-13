from django.db import models

# Create your models here.
class Car(models.Model):
    company = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    year = models.IntegerField()
    image = models.ImageField(upload_to='main_app/static/uploads/', default="")
