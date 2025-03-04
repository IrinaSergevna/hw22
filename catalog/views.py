from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from .models import Product, ContactInfo
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'page_obj'
    paginate_by = 6


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('catalog:home')


class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = ContactInfo.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print(f"{name} ({email}): {message}")
        return self.get(request, *args, **kwargs)