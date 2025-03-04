from django.urls import path, include
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ContactView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blogs/', include('blog.urls')),  # Подключение URL блога
]