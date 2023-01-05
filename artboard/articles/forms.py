from django import forms
# from django.core.exceptions import ValidationError
from martor.fields import MartorFormField

from .models import Article


class ArticleForm(forms.ModelForm):
    # text = MartorFormField()

    class Meta:
        model = Article
        fields = [
               'title',
               'category',
               'text',
            ]
