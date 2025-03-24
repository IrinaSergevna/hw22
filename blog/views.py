from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost
from django.core.mail import send_mail
from django.conf import settings
from .forms import BlogForm

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

class BlogDetailView(DetailView):
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

class BlogCreateView(CreateView):
    model = BlogPost
    form_class = BlogForm
    template_name = 'blog_create.html'
    success_url = reverse_lazy('blog:blog_list')

class BlogUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogForm
    template_name = 'blog_create.html'
    success_url = reverse_lazy('blog:blog_list')

class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')