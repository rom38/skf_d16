from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

# from markdownx.models import MarkdownxField
from martor.models import MartorField


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
    User = get_user_model()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = MartorField()
    category = models.CharField(max_length=11, choices=TYPE, default='tank')
    time_create = models.DateTimeField(auto_now_add=True)
    # upload = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f'{self.title} {self.category}'

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

    def is_owner(self, user):
        return self.author == user


class UserResponse(models.Model):
    User = get_user_model()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author} {self.text}'

    # def get_absolute_url(self):
    #     return reverse('article_detail', args=[str(self.id)])

    def is_owner(self, user):
        return self.author == user
