from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from .models import Product, Category, ContactInfo
from .forms import ProductForm, ProductModeratorForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from .services import get_products_from_cache, get_products_by_category
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class ProductListView(ListView):
    """Представление для отображения списка продуктов"""
    model = Product
    template_name = 'home.html'
    paginate_by = 6

    def get_queryset(self):
        return get_products_from_cache()

    def get_context_data(self, **kwargs):
        """Добавляет в контекст права пользователя"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['can_add_product'] = user.has_perm('catalog.add_product')
            context['can_edit_product'] = user.has_perm('catalog.can_edit_product')
            context['can_unpublish_product'] = user.has_perm('catalog.can_unpublish_product')
            context['can_delete_product'] = user.has_perm('catalog.delete_product')
        else:
            context['can_add_product'] = False
            context['can_edit_product'] = False
            context['can_unpublish_product'] = False
            context['can_delete_product'] = False
        context['categories'] = Category.objects.all()
        return context

class CategoryProductListView(ListView):
    """Представление для отображения продуктов в указанной категории"""
    model = Product
    template_name = 'category_products.html'
    paginate_by = 6

    def get_queryset(self):
        category_name = self.kwargs['category']
        products = get_products_by_category(category_name)
        return products

    def get_context_data(self, **kwargs):
        """Добавляет в контекст название категории"""
        context = super().get_context_data(**kwargs)
        category_name = self.kwargs['category']
        context['category'] = category_name.title()
        context['categories'] = Category.objects.all()
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о продукте.
    Доступно только авторизованным пользователям.
    """
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        """Добавляет в контекст права пользователя для управления продуктом."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['can_edit_product'] = user.has_perm('catalog.can_edit_product') or user == self.object.owner
            context['can_unpublish_product'] = user.has_perm('catalog.can_unpublish_product')
            context['can_delete_product'] = user.has_perm('catalog.delete_product') or user == self.object.owner
        else:
            context['can_edit_product'] = False
            context['can_unpublish_product'] = False
            context['can_delete_product'] = False
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового продукта.
    Доступно только авторизованным пользователям.
    """
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Устанавливает текущего пользователя как владельца продукта."""
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования существующего продукта.
    Доступно только авторизованным пользователям, которые являются владельцами
    продукта или имеют право `can_edit_product`.
    """
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('catalog:home')

    def get_form_class(self):
        """
        Определяет, какую форму использовать для редактирования.
        Владелец продукта использует полную форму (ProductForm),
        модератор с правом `can_unpublish_product` использует ограниченную форму (ProductModeratorForm).
        """
        user = self.request.user
        if user == self.get_object().owner:
            return ProductForm
        if user.has_perm('catalog.can_unpublish_product'):
            return ProductModeratorForm
        raise PermissionDenied()

    def form_valid(self, form):
        """Сохраняет изменения в продукте."""
        context_data = self.get_context_data()
        formset = context_data.get('formset')
        if form.is_valid() and (not formset or formset.is_valid()):
            self.object = form.save(commit=False)
            self.object.updated_by = self.request.user
            self.object.save()
            if formset:
                formset.instance = self.object
                formset.save()
        else:
            return super().form_invalid(form)
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления продукта.
    Доступно только авторизованным пользователям, которые являются владельцами
    продукта или имеют право `delete_product`.
    """
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_queryset(self):
        """
        Ограничивает список продуктов для удаления.
        Если пользователь не имеет права `delete_product`, он может удалять только свои продукты.
        """
        queryset = super().get_queryset()
        if not self.request.user.has_perm('catalog.delete_product'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        """Проверяет права пользователя на удаление продукта"""
        product = self.get_object()
        if product.owner != request.user and not request.user.has_perm('catalog.delete_product'):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class ContactView(TemplateView):
    """
    Представление для отображения и обработки контактной формы.
    """
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        """Добавляет список контактов в контекст."""
        context = super().get_context_data(**kwargs)
        context['contacts'] = ContactInfo.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает отправку контактной формы.
        Выводит данные формы в консоль и перенаправляет на страницу контактов.
        """
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print(f"{name} ({email}): {message}")
        return redirect('catalog:contact')

class UnpublishProductView(PermissionRequiredMixin, UpdateView):
    """
    Представление для снятия продукта с публикации.
    Доступно только пользователям с правом `can_unpublish_product`.
    """
    model = Product
    template_name = 'product_confirm_unpublish.html'
    success_url = reverse_lazy('catalog:home')
    permission_required = 'catalog.can_unpublish_product'

    def form_valid(self, form):
        """Снимает продукт с публикации."""
        form.instance.is_published = False
        return super().form_valid(form)