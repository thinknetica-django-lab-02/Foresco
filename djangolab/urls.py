from typing import List, cast
from django.contrib import admin
from django.urls import path, include, URLPattern
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from main.views import IndexView, ProductList, ProductDetail, ProductAdd, ProductUpdate, ProfileDetail, ProfileUpdate

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<int:pk>/', ProductDetail.as_view(), name="product-detail"),
    path('products/<int:pk>/edit/', login_required(ProductUpdate.as_view()), name="product-edit"),
    path('products/add/', login_required(ProductAdd.as_view()), name="product-add"),
    path('products/', ProductList.as_view(), name="product-list"),

    path('accounts/', include('allauth.urls')),

    path('profile/<int:pk>/edit/', login_required(ProfileUpdate.as_view()), name='profile-edit'),
    path('profile/<int:pk>/', ProfileDetail.as_view(), name="profile-detail"),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
] + cast(List[object], static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))  # Serve media files
