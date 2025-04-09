from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost
from django.core.mail import send_mail
from django.conf import settings
from .forms import BlogForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class BlogListView(ListView):
    """Представление для отображения списка статей блога."""
    model = BlogPost
    template_name = 'blog_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        """Добавляет в контекст права пользователя и список категорий."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['can_manage_blog'] = user.has_perm('blog.can_manage_blog')
        else:
            context['can_manage_blog'] = False
        return context


class BlogDetailView(DetailView):
    """Представление для отображения детальной информации о статье блога."""
    model = BlogPost
    template_name = 'blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1  # Увеличиваем счетчик просмотров
        if self.object.views_count == 100:  # Проверяем, достигнуто ли 100 просмотров
            send_mail(
                'Поздравляем с достижением!',
                f'Статья "{self.object.title}" достигла 100 просмотров!',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=True,  # Если не удаётся отправить, продолжаем работу
            )
        self.object.save()
        return self.object


class BlogCreateView(PermissionRequiredMixin, CreateView):
    """
    Представление для создания новой статьи блога.
    Доступно только пользователям с правом `can_manage_blog`.
    """
    model = BlogPost
    form_class = BlogForm
    template_name = 'blog_create.html'
    success_url = reverse_lazy('blog:blog_list')
    permission_required = 'blog.can_manage_blog'


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Представление для редактирования существующей статьи блога.
    Доступно только пользователям с правом `can_manage_blog`.
    """
    model = BlogPost
    form_class = BlogForm
    template_name = 'blog_create.html'
    success_url = reverse_lazy('blog:blog_list')
    permission_required = 'blog.can_manage_blog'


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления статьи блога.
    Доступно только пользователям с правом `can_manage_blog`.
    """
    model = BlogPost
    template_name = 'blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
    permission_required = 'blog.can_manage_blog'
