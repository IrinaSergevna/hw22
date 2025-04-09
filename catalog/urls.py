from django.urls import path, include
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, ContactView, UnpublishProductView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blogs/', include('blog.urls')),
    path('product/<int:pk>/unpublish/', UnpublishProductView.as_view(), name='product_unpublish'),
]
