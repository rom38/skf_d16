from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from .models import UserResponse


class UserResponseFilter(FilterSet):
    #category = ModelChoiceFilter(field_name='article__category', label="Поиск категории статьи")
    art_title = CharFilter(field_name='article__title', lookup_expr='icontains', label="Поиск заголовка статьи")
    resp_text = CharFilter(field_name='text', lookup_expr='icontains', label="Поиск текста отклика")
    class Meta:
        model = UserResponse
        fields = {
            # 'text': ['icontains'],
            #'article__title': ['icontains'],
            # количество товаров должно быть больше или равно
            'article__category': ['exact'],
        }
