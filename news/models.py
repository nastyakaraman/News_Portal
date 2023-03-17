from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from datetime import datetime

# Create your models here.

class Author (models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    arating = models.IntegerField(default=0)  # рейтинг

    def update_rating(self):
        prate_set=self.post_set.aggregate(postrate=Sum('rate'))
        post_rate=0
        post_rate += prate_set.get('postrate')

        crate_set = self.authorUser.comment_set.aggregate(comrate=Sum('rate'))
        com_rate = 0
        com_rate += crate_set.get('comrate')

        self.arating = post_rate*3 + com_rate
        self.save()

class Category (models.Model):

    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, through='Subscription')
    def __str__(self):
        return self.name

class Post (models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    article = 'A'
    news = 'N'
    POSTS = [
        (article, 'статья'),
        (news, 'новость'),
    ]
    type = models.CharField(max_length=1,
                                choices=POSTS,
                                default=news)

    time_in = models.DateTimeField(auto_now_add=True)#время создания
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=255,) #заголовок
    text = models.TextField(default="Пост не содержит текста")
    rate = models.IntegerField(default = 0) #рейтинг

    def __str__(self):
        return f'{self.heading.title()}\n {self.text}'

    def qset (self):
        return self.category

    def like(self):
        self.rate+=1
        self.save()

    def date(self):
        d=self.time_in.date()
        new_date = d.strftime("%d.%m.%Y")
        return new_date

    def time(self):
        t=self.time_in.time()
        new_time=t.strftime("%H:%M")
        return new_time

    def dislike(self):
        self.rate-=1
        self.save()

    def preview (self):
        prev = self.text[0:123]+'...'
        return prev

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def categories(self):
        return(list(self.category))


class PostCategory(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount


class Comment (models.Model):
    comPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    comUser = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField(default="Комментарий пуст")
    time_in = models.DateTimeField(auto_now_add=True)  # время создания
    rate = models.IntegerField(default=0)  # рейтинг

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
