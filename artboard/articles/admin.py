from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Article
from .models import UserResponse

# Register your models here.

admin.site.register(Article, MarkdownxModelAdmin)
admin.site.register(UserResponse)
