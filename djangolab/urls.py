from django.contrib import admin
from django.urls import path, include

from main.views import IndexView, ProductList, ProductDetail

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<int:pk>/', ProductDetail.as_view(), name="product-detail"),
    path('products/', ProductList.as_view(), name="product-list"),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]
