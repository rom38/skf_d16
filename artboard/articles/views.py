# from django.shortcuts import render
import logging
import json
import uuid
import os

from django.views.generic import (
            ListView, DetailView, CreateView,
            UpdateView, DeleteView)
            # UpdateView, DeleteView, View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import Article
from .forms import ArticleForm




from martor.utils import LazyEncoder



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


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and is_ajax(request=request):
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size)s MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))
