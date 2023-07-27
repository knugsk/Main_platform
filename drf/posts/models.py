from django.db import models
from users.models import member
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name="카테고리", max_length=20)
    
    class Meta:
        verbose_name = '카테고리 명'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    user = models.ForeignKey(member, verbose_name='작성자', on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, verbose_name='카테고리', on_delete=models.CASCADE)
    title = models.CharField(verbose_name="제목", max_length=255)
    content = models.TextField(verbose_name="내용")
    file_uploaded = models.FileField(verbose_name="첨부 파일", null=True, upload_to="posting")

    published_date = models.DateTimeField(default=timezone.now)

