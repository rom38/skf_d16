from django.urls import path
# Импортируем созданное нами представление
from .views import (
   ArticleList, ArticleDetail, ArticleCreate,
   ArticleUpdate, ArticleDelete, UserResponseCreate,
   markdown_uploader
   )


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', ArticleList.as_view(), name='article_list'),
   path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
#    path('search/', NewsSearch.as_view()),
   path('create/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('<int:pk>/create_response/', UserResponseCreate.as_view(), name='response_create'),
   path(
      'api/uploader/', markdown_uploader, name='markdown_uploader_page'
   ),
#    path('categories/<int:pk>', CategoryNewsList.as_view(), name='news_category'),
#    path('categories/<int:pk>/subscribe/', Subscribe.as_view(), name='news_subscribe'),
#    path('new_author/', BeAuthor.as_view(), name='new_author'),
]
