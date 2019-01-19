from django.db import models

# Create your models here.

class food(models.Model):
    starter_name = models.CharField(max_length=30)
    dish_name = models.CharField(max_length=30)
    desert_name = models.CharField(max_length=30)
    starter_calories = models.FloatField()
    dish_calories = models.FloatField()
    desert_calories = models.FloatField()
    sum_calories = models.FloatField()
