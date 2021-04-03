from django.db.models import Count
from django.views.generic import TemplateView, ListView, DetailView, UpdateView

from django.contrib.auth.models import User
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
    paginate_by = 10

    def __init__(self):
        super().__init__()
        self.getfilters = list()  # List of get filters

    def get_queryset(self):
        qs = Product.objects.all()
        # Tag filter
        tag = self.request.GET.get('tag', None)
        if tag:
            qs = qs.filter(tag__pk=tag)
            self.getfilters.append('tag='+ tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter items
        context['filters'] = dict()
        # All tags used by products
        context['filters']['tags'] = Tag.objects.annotate(pro_quant=Count("products__pk")).filter(pro_quant__gt=0)
        context['getfilters'] = '&'.join(self.getfilters)
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProfileUpdate(UpdateView):
    model = User
    template_name = 'profile.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = '/'