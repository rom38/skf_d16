from django.db.models.signals import m2m_changed, post_save
# импортируем нужный декоратор
from django.dispatch import receiver
from django.core.cache import cache

# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
from .models import Article, UserResponse
# from news_portal.settings import SITE_URL, DEFAULT_FROM_EMAIL
from .tasks import send_notify, send_notify_responser

@receiver(post_save, sender=UserResponse)
def send_notify_author_article(sender, instance: UserResponse, created, **kwargs):
    subscribers: list[str] = []
    # если отклик создан, извещаем автора статьи
    if created:
        subscribers.append(instance.article.author.email)
        send_notify.delay(instance.article.title, instance.text, instance.article.author.username,
            subscribers)
    # если отклик изменен и статус - True извещаем, автора отклика
    elif instance.status:
        subscribers.append(instance.author.email)
        send_notify_responser.delay(instance.article.title, instance.article.get_absolute_url(),
                                    instance.text, instance.author.username,
            subscribers)
        