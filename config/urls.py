from django.contrib import admin
from django.urls import path, include
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls', namespace='catalog'))
]
