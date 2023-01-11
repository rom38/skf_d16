# import time
import datetime

from celery import shared_task

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from artboard.settings import  DEFAULT_FROM_EMAIL, SITE_URL

from .models import Article, UserResponse


@shared_task
def news_notify_weekly_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    articles = Article.objects.filter(time_create__gte=last_week)
    subscribers = set(articles.values_list('author__email', flat=True))
    # subscribers
    print(subscribers)
    html_content = render_to_string(
        'articles_notify_weekly.html', {
            # 'link': f'{SITE_URL}/news/{pk}',
            'link': f'{SITE_URL}',
            'articles': articles,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='Статьи добавленные за неделю',
        from_email=DEFAULT_FROM_EMAIL,
        to=list(subscribers),
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    #  Your job processing logic here...
    print('hello from job')


@shared_task
def send_notify(article_title, response_text, username, subscribers):
    html_content = render_to_string(
        'response_notify.html', {
            'article_title': article_title,
            'username': username,
            'response_text': response_text,
            'link': f'{SITE_URL}/articles/response_list/'
        }
    )
    msg = EmailMultiAlternatives(
        subject='Новый отклик на статью',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
