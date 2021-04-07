from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from main.views import IndexView, ProductList, ProductDetail, ProductAdd, ProductUpdate, ProfileUpdate

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<int:pk>/', ProductDetail.as_view(), name="product-detail"),
    path('products/<int:pk>/edit/', ProductUpdate.as_view(), name="product-edit"),
    path('products/add/', ProductAdd.as_view(), name="product-add"),
    path('products/', ProductList.as_view(), name="product-list"),

    path('accounts/profile/<int:pk>/', login_required(ProfileUpdate.as_view()), name='profile-update'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]
