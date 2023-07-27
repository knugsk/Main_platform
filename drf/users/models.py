from django.db import models

# Create your models here.

class member(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    stu_id = models.IntegerField(verbose_name="학번")
    first_name = models.CharField(verbose_name="성", max_length=30)
    last_name = models.CharField(verbose_name="이름", max_length=30)

    password = models.CharField(max_length=255)
    