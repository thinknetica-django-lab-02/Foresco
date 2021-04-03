from django.forms.models import inlineformset_factory

from django.contrib.auth.models import User
from .models import Profile

ProfileFormset = inlineformset_factory(User, Profile, fields=())
