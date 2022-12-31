from django import forms
# from django.core.exceptions import ValidationError

from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = [
               'title',
               'text',
               'category',
            ]
