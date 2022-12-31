from django.urls import path
# from django.contrib.auth import views as auth_views
# Импортируем созданное нами представление
from .views import ArtLogoutView
from .views import ArtLoginView


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    path('logout/', ArtLogoutView.as_view(), name='logout'),
    path('login/', ArtLoginView.as_view(), name='login'),
#    path('', ArticleList.as_view(), name='article_list'),
#    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
# #    path('search/', NewsSearch.as_view()),
#    path('create/', ArticleCreate.as_view(), name='article_create'),
#    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
#    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
#    path('categories/<int:pk>', CategoryNewsList.as_view(), name='news_category'),
#    path('categories/<int:pk>/subscribe/', Subscribe.as_view(), name='news_subscribe'),
#    path('new_author/', BeAuthor.as_view(), name='new_author'),
]
