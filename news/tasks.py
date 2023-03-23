from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import Post, Subscription
from django.contrib.auth.models import User
from django.conf import settings
from celery import Celery
from django.template.loader import render_to_string

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

app = Celery('News_Portal')
@app.task
def send_weeklynews():
    import datetime
    today = datetime.datetime.now()
    lastweek = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=lastweek)
    categories = set(posts.values_list('category__id', flat=True))
    emailed = []
    subscribers = set(Subscription.objects.filter(category__in=categories).values_list('user__email', flat=True))
    for subscriber in subscribers:
        user_id = User.objects.get(email=subscriber).id
        categories_for_subscriber = set(
            Subscription.objects.filter(user=user_id).values_list('category__id', flat=True))
        posts_for_subscriber = posts.filter(category__in=categories_for_subscriber)
        html_content = render_to_string(
            'weekly_news.html',
            {
                'posts': posts_for_subscriber,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Еженедельная рассылка по любимым категориям',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()