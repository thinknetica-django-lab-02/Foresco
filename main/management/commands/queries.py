from django.core.management.base import BaseCommand

from main.models import Tag, Category, Product, Seller, Price


class Command(BaseCommand):
    help = 'Creates items im main models'

    def handle(self, *args, **options):
        # Create tags
        t1 = Tag(tag='Дети')
        t1.save()
        t2 = Tag(tag='Взрослые')
        t2.save()
        t3 = Tag(tag='Домашние животные')
        t3.save()

        # Create categories
        c1 = Category(category_name='Продукты питания')
        c1.save()
        c2 = Category(category_name='Одежда')
        c2.save()
        c3 = Category(category_name='Обувь')
        c3.save()
        c4 = Category(category_name='Услуги')
        c4.save()

        # Edit categories
        c1.description = 'Продукты для употребления в пишу'
        c1.save()

        # Create products
        p1 = Product(product_name='Мороженое',  product_type='item')
        p1.save()
        p1.category.set([c1, ])
        p2 = Product(product_name='Сандалии', description='Легкая летняя кожаная обувь')
        p2.save()
        p2.category.set([c3, ])
        p3 = Product(product_name='Стрижка', product_type='service')
        p3.save()
        p3.category.set([c4, ])

        # Edit products
        p1.tag.add(t1, t2)
        p1.save()
        p3.tag.add(t1, t2, t3)
        p1.save()

        # Create sellers
        s1 = Seller.objects.create(seller_name='Магнит')
        s1 = Seller.objects.create(seller_name='Пятерочка')
        s1 = Seller.objects.create(seller_name='1001 туфелька')

        # Edit sellers
        Seller.objects.exclude(
            seller_name='1001 туфелька'
        ).update(
            description='Всероссийская сеть продуктовых магазинов'
        )

        # Create prices
        s1 = Seller.objects.get(seller_name='Магнит')
        pr1 = Price(seller=s1, product=p1, price=58.6)
        pr1.save()

        # Edit prices
        pr1.comment = 'Обратить внимание на срок годности'
        pr1.save()
