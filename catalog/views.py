from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Product, ContactInfo
from .forms import ProductForm


# def home(request):
#     latest_products = Product.objects.order_by("-created_at")[
#         :5
#     ]  # Выборка 5 последних продуктов
#     return render(request, "home.html", {"latest_products": latest_products})

def home(request):
    # Получаем все товары (можно изменить фильтрацию или сортировку)
    product_list = Product.objects.all()

    # Создаем пагинатор: 6 товаров на странице
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')  # Получаем номер страницы
    page_obj = paginator.get_page(page_number)  # Получаем товары для текущей страницы

    return render(request, "home.html", {"page_obj": page_obj})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print(f"{name} ({email}): {message}")
    return render(request, "contact.html")


def contact_page(request):
    contacts = ContactInfo.objects.all()  # Загрузка всех контактов
    return render(request, "contact.html", {"contacts": contacts})  # Передача в шаблон


def index(request):
    return render(request, 'base.html')


def product_list(request):
    products = Product.object.all()
    return render(request, 'product_detail.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})