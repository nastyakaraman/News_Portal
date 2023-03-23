from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import Post, Subscription
from django.conf import settings
import time


@shared_task
def send_newarticle(oid):
    print(oid)
    post = Post.objects.get(pk = oid)
    subscribers = set(Subscription.objects.filter(
        category__in=post.category.all()).values_list('user__email', flat=True))
    if subscribers:
        html_content = (
            f'Привет! В твоей любимой категории вышел новый пост: "{post.heading}"<br>'
            f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
            f'Ссылка на пост</a>')

        for subscriber in subscribers:
            msg = EmailMultiAlternatives(
                subject='Новый пост в вашей любимой категории',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber]
                )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
