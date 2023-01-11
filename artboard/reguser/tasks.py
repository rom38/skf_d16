from celery import shared_task

from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from artboard.settings import  DEFAULT_FROM_EMAIL


@shared_task
def send_email_verify(usr_id, domain, rnd_str_email):
    User = get_user_model()
    user = User.objects.get(pk=usr_id)
    context = {
        'user': user,
        'domain': domain,
        'rnd_str': rnd_str_email,
    }
    message = render_to_string(
        'registration/verify_email.html',
        context=context,
    )

    msg = EmailMultiAlternatives(
        subject='verify email',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(message, 'text/html')
    msg.send()
    