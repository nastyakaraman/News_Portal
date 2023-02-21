from django.views.generic import ListView, DetailView
from .models import Post
from .filters import ProductFilter

class PostsList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'