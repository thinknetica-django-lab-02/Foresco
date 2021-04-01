from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django import forms

from main.models import Product, Tag


class IndexView(TemplateView):
    """Main page"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['turn_on_block'] = True
        context['content'] = 'Добро пожаловать в наш Интернет-магазин!'
        context['title'] = 'Магазин "Продать быстрее"'
        context['user'] = getattr(self.request, 'user', 'Unknown')

        return context


class ProductList(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'product_list.html'


class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'
