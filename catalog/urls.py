from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contact, contact_page

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact, name="contact"),
    path("contacts/", contact_page, name="contact_page"),
]