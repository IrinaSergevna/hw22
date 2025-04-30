from django.contrib import admin
from .models import Product, Category, ContactInfo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")  # Отображение id и name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "category",
    )  # Отображение id, name, price и category
    list_filter = ("category",)  # Фильтрация по категории
    search_fields = ("name", "description")  # Поиск по name и description


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "address",
    )  # Отображение name, phone, email, address
    search_fields = ("phone", "email", "address")  #  Поиск по phone, email, address
