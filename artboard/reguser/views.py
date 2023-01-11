from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.views import View
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site



from articles.models import Article
from .forms import UserCreationForm, EmailVerifyForm
from .tasks import send_email_verify
# Create your views here.

User = get_user_model()


class ArtLogoutView(LogoutView):
    next_page = 'article_list'


class ArtLoginView(LoginView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        print(f'user_name: {user.username}')
        print(f'email_verify: {user.email_verify}')
        if not user.email_verify:
            RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"
            rnd_str_for_email = get_random_string(length=7, allowed_chars=RANDOM_STRING_CHARS)
            self.request.session[rnd_str_for_email] = [user.id, token_generator.make_token(user)]
            current_site = get_current_site(self.request)
            send_email_verify.delay(
                usr_id=user.id, domain=current_site.domain,
                rnd_str_email=rnd_str_for_email
                )
            return redirect(reverse('verify_email'))

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
            # send_email_for_verify_2(request, user)
            RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"
            rnd_str_for_email = get_random_string(length=7, allowed_chars=RANDOM_STRING_CHARS)
            request.session[rnd_str_for_email] = [user.id, token_generator.make_token(user)]
            current_site = get_current_site(request)
            send_email_verify.delay(
                usr_id=user.id, domain=current_site.domain,
                rnd_str_email=rnd_str_for_email
                )
            return redirect(reverse('verify_email'))
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
                    'возможно вы ошиблись, либо сессия закончилась, повторите ввод, либо повторно'
                    'выполните вход'
                    )
                return render(request, self.template_name, context)

            user = self.get_user(user_id)
            if user is not None and token_generator.check_token(user, token):
                user.email_verify = True
                # add user to common_user group
                common_users, create = Group.objects.get_or_create(name="common_user")
                if create:
                    content_type = ContentType.objects.get_for_model(Article)
                    article_permissions = Permission.objects.filter(content_type=content_type)
                    for perm in article_permissions:
                        common_users.permissions.add(perm)
                user.groups.add(common_users)
                user.save()
                login(request, user)
                return redirect(reverse('confirm_email'))
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
