from django.contrib import admin
from django.urls import path, include

from main.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]
