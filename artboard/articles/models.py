from django.contrib.auth.models import User

from markdownx.models import MarkdownxField

from django.db import models

# Create your models here.


class Article(models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('medic', 'Хилы'),
        ('dd', 'ДД'),
        ('privater', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = MarkdownxField()
    category = models.CharField(max_length=11, choices=TYPE, default='tank')
    # upload = models.FileField(upload_to='uploads/')


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

