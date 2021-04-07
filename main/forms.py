from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from django.contrib.auth.models import User
from .models import Profile, Product


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ('user', )

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise ValidationError("Возраст должен быть больше 18 лет!")
        return age


ProfileFormset = inlineformset_factory(User, Profile, form=ProfileForm, extra=1)


class ProductForm(ModelForm):

    class Meta:
        model = Product
        exclude = ()


TagFormSet = inlineformset_factory(Product, Product.tag.through, form=ProductForm, extra=1)

CategoryFormSet = inlineformset_factory(Product, Product.category.through, form=ProductForm, extra=1)
