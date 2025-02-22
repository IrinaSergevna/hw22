from django.contrib import admin
from django.urls import path, include
from catalog.apps import CatalogConfig
from django.conf.urls.static import static
from django.conf import settings
from catalog.views import contact, contact_page

app_name = CatalogConfig.name

urlpatterns = [
    path("admin/", admin.site.urls),
    path("contact/", contact, name="contact"),
    path("contacts/", contact_page, name="contact_page"),
    path("", include(("catalog.urls", "catalog"), namespace="catalog")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)