from django.urls import path
from django.views.generic import TemplateView
# from django.contrib.auth import views as auth_views
# Импортируем созданное нами представление
from .views import ArtLogoutView
from .views import ArtLoginView
from .views import RegUserView
from .views import EmailVerify


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    path('logout/', ArtLogoutView.as_view(), name='logout'),
    path('login/', ArtLoginView.as_view(), name='login'),
    path('reg_user/', RegUserView.as_view(), name='reg_user'),
    path(
        'confirm_email/',
        TemplateView.as_view(template_name='registration/confirm_email.html'),
        name='confirm_email'
    ),
    path(
        'verify_email/',
        EmailVerify.as_view(),
        name='verify_email',
            ),
    path(
        'invalid_verify/',
        TemplateView.as_view(template_name='registration/invalid_verify.html'),
        name='invalid_verify'
    ),
    path(
        'not_verified_email/',
        TemplateView.as_view(template_name='registration/not_verified_email.html'),
        name='not_verified_email'
    ),

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
