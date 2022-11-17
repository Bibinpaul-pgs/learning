from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveBigIntegerField()
    roll_num = models.PositiveIntegerField()
    degree = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)

    class Meta:
        unique_together = ('name', 'roll_num',)