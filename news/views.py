from django.views.generic import ListView, DetailView
from .models import Post

class PostsList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'