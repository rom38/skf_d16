from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode

from .forms import UserCreationForm, EmailVerifyForm
from .utils import send_email_for_verify_2
# Create your views here.

User = get_user_model()


class ArtLogoutView(LogoutView):
    next_page = 'article_list'


class ArtLoginView(LoginView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        print(f'user_name: {user.username}')
        print(f'user_name: {user.email_verify}')
        if not user.email_verify:
            send_email_for_verify_2(self.request, user)
            return redirect('verify_email')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = reverse_lazy('article_list')
        return context


class RegUserView(View):
    template_name = 'registration/reg_user.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            # email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            # user = authenticate(email=email, password=password)
            user = authenticate(username=username, password=password)
            send_email_for_verify_2(request, user)
            return redirect('verify_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class EmailVerify(View):
    template_name = 'registration/verify_token.html'

    def get(self, request):
        context = {
            'form': EmailVerifyForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = EmailVerifyForm(request.POST)
        context = {
            'form': form,
            'error': ''
        }

        if form.is_valid():
            rnd_str = form.cleaned_data.get('rnd_str')
            try:
                user_id, token = request.session.pop(rnd_str)
            except KeyError:
                context['error'] = (
                    'такого токена не существует, '
                    'возможно вы ошиблись, повторите ввод, либо повторно'
                    'выполните вход'
                    )
                return render(request, self.template_name, context)

            user = self.get_user(user_id)
            if user is not None and token_generator.check_token(user, token):
                user.email_verify = True
                user.save()
                login(request, user)
                return redirect('confirm_email')
        return render(request, self.template_name, context)

    @staticmethod
    def get_user(user_id):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user
