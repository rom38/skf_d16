from django.contrib import admin
from django.db import models

from martor.widgets import AdminMartorWidget

from .models import Article
from .models import UserResponse

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


admin.site.register(Article, ArticleAdmin)
admin.site.register(UserResponse)
