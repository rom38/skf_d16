from django import forms

from .models import Article, UserResponse


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = [
               'title',
               'category',
               'text',
            ]


class UserResponseForm(forms.ModelForm):

    class Meta:
        model = UserResponse
        fields = [
               'text',
            ]
