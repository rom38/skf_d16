from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator as token_generator


def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': token_generator.make_token(user),
    }
    message = render_to_string(
        'registration/verify_email.html',
        context=context,
    )
    email = EmailMessage(
        'Veryfi email',
        message,
        to=[user.email],
    )
    email.send()


def send_email_for_verify_2(request, user):
    RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"
    rnd_str_for_email = get_random_string(length=7, allowed_chars=RANDOM_STRING_CHARS)
    request.session[rnd_str_for_email] = [user.id, token_generator.make_token(user)]
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'rnd_str': rnd_str_for_email,
    }
    message = render_to_string(
        'registration/verify_email.html',
        context=context,
    )
    email = EmailMessage(
        'Veryfi email',
        message,
        to=[user.email],
    )
    email.send()
