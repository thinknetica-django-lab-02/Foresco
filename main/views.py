from django.db.models import Count
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from main.models import Product, Tag
from .forms import UserForm, ProductForm, ProfileFormset, TagFormSet, CategoryFormSet

# Register signals
import main.signals


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


class ProductAdd(CreateView):
    model = Product
    fields = ('product_name', 'product_type', 'description', 'certified')
    template_name = 'product_add.html'


class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product.html'
    success_url = None

    def get_context_data(self, **kwargs):
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

    def get_success_url(self):
        return reverse_lazy('product-edit', kwargs={'pk': self.object.pk})


class ProfileDetail(DetailView):
    queryset = User.objects.all().select_related('profile')
    context_object_name = 'profile'
    template_name = 'profile_detail.html'


class ProfileUpdate(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'profile.html'
    success_url = None

    def get_context_data(self, **kwargs):
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

    def get_success_url(self):
        return reverse_lazy('profile-update', kwargs={'pk': self.object.pk})
