from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

# Model storing FlatPages pages
from django.contrib.flatpages.models import FlatPage


class FlatPageAdminForm(forms.ModelForm):
    """Form for FlatPage editing"""
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdmin(admin.ModelAdmin):
    """Admin class for FlatPage model"""
    form = FlatPageAdminForm


# Unregister default admin class for FlatPage model
admin.site.unregister(FlatPage)

# Register admin class for FlatPage model
admin.site.register(FlatPage, FlatPageAdmin)
