import factory
import random
from django.core.management.base import BaseCommand

from main.models import Product, Seller, Price


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('product_name',)

    product_name = factory.Sequence(lambda n: f"Товар {n:03d}")
    product_type = factory.Iterator(['service', 'item'])
    description = 'fake product'


class SellerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Seller
        django_get_or_create = ('seller_name',)

    seller_name = factory.Sequence(lambda n: f"Продавец {n:03d}")
    description = 'fake seller'


def get_random():
    return random.random()


class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price

    seller = factory.SubFactory(SellerFactory)
    product = factory.SubFactory(ProductFactory)
    price = factory.LazyFunction(get_random)
    article = factory.Sequence(lambda n: f"{n:03d}")
    comment = 'fake price'


class Command(BaseCommand):
    help = 'Put random data into models'

    def handle(self, *args, **options):
        PriceFactory.create_batch(size=10)
