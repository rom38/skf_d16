from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# Create your views here.


class ArtLogoutView(LogoutView):
    next_page = 'article_list'


class ArtLoginView(LoginView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = reverse_lazy('article_list')
        return context


# {{ request.path }}  #  -without GET parameters
# {{ request.get_full_path }}  # - with GET parameters
