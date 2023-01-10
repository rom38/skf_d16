from django.urls import path
# Импортируем созданное нами представление
from .views import (
   ArticleList, ArticleDetail, ArticleCreate,
   ArticleUpdate, ArticleDelete, UserResponseCreate,
   UserResponseList, UserResponseGood,markdown_uploader,
   UserResponseDelete
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
   path('<int:pk>/response_create/', UserResponseCreate.as_view(), name='response_create'),
   path('responses/<int:pk_resp>/good', UserResponseGood.as_view(),
        name='response_good'),
   path('responses/<int:pk_resp>/delete', UserResponseDelete.as_view(),
        name='response_delete'),
   path('response_list/', UserResponseList.as_view(),
        name='response_list'),
   path(
      'api/uploader/', markdown_uploader, name='markdown_uploader_page'
   ),
#    path('categories/<int:pk>', CategoryNewsList.as_view(), name='news_category'),
#    path('categories/<int:pk>/subscribe/', Subscribe.as_view(), name='news_subscribe'),
#    path('new_author/', BeAuthor.as_view(), name='new_author'),
]
