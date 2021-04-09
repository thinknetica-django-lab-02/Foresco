from django.db.models import Count
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from main.models import Product, Tag, Profile
from .forms import ProfileForm, UserFrom, ProfileFormset


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
    form_class = UserFrom
    template_name = 'profile.html'
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(ProfileUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['profile'] = ProfileFormset(self.request.POST, instance=self.object)
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
