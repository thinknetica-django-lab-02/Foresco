from django import forms
from django.contrib import admin
from django.contrib.auth.models import Permission  # Для возможности администрировать права
from ckeditor.widgets import CKEditorWidget

# Model storing FlatPages pages
from django.contrib.flatpages.models import FlatPage

from .models import Profile, Product, Price


class FlatPageAdminForm(forms.ModelForm):
    """Form for FlatPage editing"""
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdmin(admin.ModelAdmin):
    """Admin class for FlatPage model"""
    form = FlatPageAdminForm


admin.site.register(Permission)

# Unregister default admin class for FlatPage model
admin.site.unregister(FlatPage)

# Register admin class for FlatPage model
admin.site.register(FlatPage, FlatPageAdmin)

admin.site.register(Profile)


def make_unnoticed(modeladmin, request, queryset):
    queryset.update(noticed=False)
make_unnoticed.short_description = "Пометить как новинки для оповещения"


def make_noticed(modeladmin, request, queryset):
    queryset.update(noticed=True)
make_noticed.short_description = "Убрать из оповещения"


class ProductPriceInline(admin.TabularInline):
    model = Price


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_type']
    ordering = ['product_name']
    list_filter = ['certified', 'product_type', 'noticed']
    actions = [make_unnoticed, make_noticed]

    fieldsets = (
        (None, {
            'fields': ('product_name', 'product_type', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('certified', 'noticed'),
        }),
        ('Tags and categories', {
            'classes': ('collapse',),
            'fields': ('tag', 'category'),
        }),
    )
    inlines = [
        ProductPriceInline,
    ]


admin.site.register(Product, ProductAdmin)
