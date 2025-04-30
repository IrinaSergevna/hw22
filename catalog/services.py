from django.core.cache import cache
from django.conf import settings
from .models import Product

def get_products_from_cache():
    """Получает данные по продуктам из кэша, если кэш пуст, получает данные из бд."""
    if not settings.CACHE_ENABLED:
        return Product.objects.all()

    key = 'products_list_all'
    products = cache.get(key)
    if products is None:
        products = Product.objects.all()
        cache.set(key, products, timeout=300)
    return products

def get_products_by_category(category_name):
    """Возвращает список всех продуктов в указанной категории."""
    if not settings.CACHE_ENABLED:
        return Product.objects.filter

    key = f'products_category_{category_name}'
    products = cache.get(key)
    if products is None:
        products = Product.objects.filter(category__name__iexact=category_name, is_published=True)
        cache.set(key, products, timeout=60 * 5)
    return products
