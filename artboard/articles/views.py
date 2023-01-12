# from django.shortcuts import render
import logging
import json
import uuid
import os

from django.views.generic import (
            ListView, DetailView, CreateView,
            UpdateView, DeleteView, View)
            # UpdateView, DeleteView, View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse


from .models import Article, UserResponse
from .forms import ArticleForm, UserResponseForm




from martor.utils import LazyEncoder



# Create your views here.

logger = logging.getLogger(__name__)

# перегрузка класса, удалять и изменять статью может только ее автор
# миксин нужен, чтобы нельзя было перейти по url
class OwnerPermissionRequiredMixin(PermissionRequiredMixin):

    def has_permission(self):
        perms = self.get_permission_required()
        # if not self.get_object().postAuthor.authorUser.id == self.request.user.id:
        #     raise PermissionDenied()
        is_owner_func = getattr(self.get_object(), 'is_owner', None)
        if is_owner_func is None:
            raise RuntimeError('mixin requires model {} to provide is_owner function)'.format(self.get_object()))
        if not self.get_object().is_owner(self.request.user):
            return self.handle_no_permission()
        return self.request.user.has_perms(perms)


class ArticleCreate(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = ArticleForm
    # permission_required = ('articles.add_article',)
    # модель статей
    model = Article
    # и новый шаблон, в котором используется форма.
    template_name = 'article_edit.html'
    # raise_exception = True

    # автоматически делаем авторизованного пользователя автором
    def form_valid(self, form):
        User = get_user_model()
        form.instance.author = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class ArticleDetail(DetailView):
    template_name = 'article_detail.html'
    context_object_name = 'article'
    model = Article
    # queryset = Article.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['author_user'] = False
        if not user.is_anonymous and self.get_object().is_owner(user):
            context['author_user'] = True
        responses = self.get_object().responses.filter(status=True)
        context['responses'] = responses
        return context


class ArticleUpdate(OwnerPermissionRequiredMixin, UpdateView):
    permission_required = ('articles.change_article',)
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'
    context_object_name = 'article'


class ArticleDelete(OwnerPermissionRequiredMixin, DeleteView):
    permission_required = ('articles.delete_article',)
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



class UserResponseCreate(LoginRequiredMixin, CreateView):
    form_class = UserResponseForm
    # permission_required = ('articles.add_article',)
    model = UserResponse
    template_name = 'response_edit.html'

    # автоматически делаем авторизованного пользователя автором
    def form_valid(self, form):
        # User = get_user_model()
        # form.instance.author = User.objects.get(id=self.request.user.id)
        form.instance.author = self.request.user
        form.instance.article = Article.objects.get(pk = self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_list')


class UserResponseList(LoginRequiredMixin, ListView):
    model = UserResponse
    ordering = '-time_create'
    template_name = 'response_list.html'
    context_object_name = 'responses'
    paginate_by = 10
    # фильтруем отклики на статьи только авторизованного
    # пользоавателя

    def get_queryset(self):
        return super().get_queryset().filter(article__author=self.request.user)

class UserResponseDelete(LoginRequiredMixin, View):
    # permission_required = ('news.delete_post',)
    model = UserResponse

    def get(self, request, pk_resp):
        query = UserResponse.objects.filter(pk=pk_resp, article__author=request.user)
        if query:
            query.delete()
            return HttpResponseRedirect(reverse('response_list'))
        else:
            return HttpResponseNotFound()


class UserResponseGood(LoginRequiredMixin, View):
    # permission_required = ('news.delete_post',)
    model = UserResponse

    def get(self, request, pk_resp):
        query = UserResponse.objects.filter(pk=pk_resp, article__author=request.user)
        if query:
            query[0].status=True
            query[0].save()
            return HttpResponseRedirect(reverse('response_list'))
        else:
            return HttpResponseNotFound()


# rewrite depricated request.is_ajax() for jquery
# need to replace  request.accept('')
def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


# view for upload images to text field
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

            # replace '_size' to 'size'
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
