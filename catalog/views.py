from django.shortcuts import render
from catalog.models import Product, ContactInfo


def home(request):
    latest_products = Product.objects.order_by("-created_at")[
        :5
    ]  # Выборка 5 последних продуктов
    return render(request, "home.html", {"latest_products": latest_products})


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