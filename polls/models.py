from django.db import models

# Create your models here.
class Question(models.Model):
    room = models.CharField(max_length=4)
    ChName = models.CharField(max_length=20)
    begin_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    rent_amt = models.IntegerField(default=0)
