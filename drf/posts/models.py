from django.db import models
from users.models import CustomUser
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='author')
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='posts')
    body = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    # files = models.FileField(upload_to='post_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             related_name='comments',
                             on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self',
                                       related_name='replies',
                                       on_delete=models.CASCADE,
                                       null=True,
                                       blank=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.author}님이 {self.post.title}에 작성한 댓글"

class File(models.Model):
    file = models.FileField(upload_to='')
    post = models.ForeignKey(Post, related_name='files', on_delete=models.CASCADE)
