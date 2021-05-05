from typing import Dict, Any
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.contrib.auth.models import User
from main.models import Product, Tag, ViewCounter
from .forms import UserForm, ProductForm, ProfileFormset, TagFormSet, CategoryFormSet

# Register signals
import main.signals


class CounterMixin(DetailView):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        ViewCounter.count_view(request.path)
        return super().get(request, *args, **kwargs)


@method_decorator(cache_page(60 * 24), name='dispatch')
class IndexView(TemplateView):
    """Main page"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super(TemplateView, self).get_context_data(**kwargs)

        context['turn_on_block'] = self.request.user.is_authenticated
        context['content'] = 'Добро пожаловать в наш Интернет-магазин!'
        context['title'] = 'Магазин "Продать быстрее"'
        context['user'] = getattr(self.request, 'user', 'Unknown')

        return context


@method_decorator(cache_page(60 * 2), name='dispatch')
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
            self.getfilters.append('tag=' + tag)
        return qs

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Filter items
        context['filters'] = dict()
        # All tags used by products
        context['filters']['tags'] = Tag.objects.annotate(pro_quant=Count("products__pk")).filter(pro_quant__gt=0)
        context['getfilters'] = '&'.join(self.getfilters)
        return context


class ProductAdd(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ('product_name', 'product_type', 'description', 'certified')
    template_name = 'product_add.html'
    permission_required = 'main.add_product'


class ProductDetail(CounterMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        view_count = cache.get('view_count')
        if view_count is None:
            view_count = ViewCounter.get_count(self.request.path)
            cache.set('view_count', view_count, timeout=60)
        context['view_count'] = view_count
        return context


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product.html'
    success_url = None
    object = Product
    permission_required = 'main.change_product'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super(ProductUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['tag'] = TagFormSet(self.request.POST, instance=self.object)
            data['category'] = CategoryFormSet(self.request.POST, instance=self.object)
        else:
            data['tag'] = TagFormSet(instance=self.object)
            data['category'] = CategoryFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tag = context['tag']
        category = context['category']
        obj = form.save()
        if tag.is_valid():
            tag.instance = obj
            tag.save()
        else:
            return self.render_to_response(context)
        if category.is_valid():
            category.instance = obj
            category.save()
        else:
            return self.render_to_response(context)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse_lazy('product-edit', kwargs={'pk': self.object.pk})


class ProfileDetail(CounterMixin, DetailView):
    queryset = User.objects.all().select_related('profile')
    context_object_name = 'profile'
    template_name = 'profile_detail.html'


class ProfileUpdate(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'profile.html'
    success_url = None
    object = User

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data = super(ProfileUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['profile'] = ProfileFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['profile'] = ProfileFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        profile = context['profile']
        obj = form.save()
        if profile.is_valid():
            profile.instance = obj
            profile.save()
        else:
            return self.render_to_response(context)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse_lazy('profile-update', kwargs={'pk': self.object.pk})
