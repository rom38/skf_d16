# from django.shortcuts import render
import logging

from django.views.generic import (
            ListView, DetailView, CreateView,
            UpdateView, DeleteView)
            # UpdateView, DeleteView, View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .models import Article
from .forms import ArticleForm

# Create your views here.

logger = logging.getLogger(__name__)


class ArticleCreate(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = ArticleForm
    # permission_required = ('articles.add_article',)
    # модель статей
    model = Article
    # и новый шаблон, в котором используется форма.
    template_name = 'article_edit.html'
    # raise_exception = True

    def form_valid(self, form):
        User = get_user_model()
        form.instance.author = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class ArticleDetail(DetailView):
    template_name = 'article_detail.html'
    context_object_name = 'article'
    model = Article
    # queryset = Article.objects.all()


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    # permission_required = ('articles.update_article',)
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'
    context_object_name = 'article'


class ArticleDelete(LoginRequiredMixin, DeleteView):
    # permission_required = ('articles.delete_article',)
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')


class ArticleList(ListView):
    model = Article
    ordering = '-time_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'list_articles.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'articles'
    # Отфильтровываем из статей и новостей только новости
    paginate_by = 10

    # def get_queryset(self):
    #     return super().get_queryset().filter(post_type=Post.news)

    def get_context_data(self, **kwargs):
        # test logger
        logger.warning("Warning from view listview ")
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        # context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # context['next_sale'] = None
        user = self.request.user
        context['author_user'] = False
        if not user.is_anonymous and Article.objects.filter(author=user).exists():
            context['author_user'] = True
        return context
