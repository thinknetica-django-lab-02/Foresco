from django.db import models


class Tag(models.Model):
    """Тэги"""
    tag = models.CharField(max_length=20, null=False, unique=True, verbose_name='Тег')
    description = models.TextField(blank=True, null=True, verbose_name='Описание тега')

    def __str__(self):
        return f'{self.tag} ({self.description})'

    class Meta:
        ordering = ['tag']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Category(models.Model):
    """Категории"""
    category_name = models.CharField(max_length=200, null=False, unique=True, verbose_name='Наименование категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание категории')


    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name']
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class Product(models.Model):
    """Товары"""
    TYPECHOICES = (
            ('service', 'Услуга'),
            ('item', 'Предмет'),
        )
    product_name = models.CharField(max_length=200, null=False, unique=True, verbose_name='Наименование товара')
    product_type = models.CharField(max_length=7, null=False, default='item', choices=TYPECHOICES,
                                    verbose_name='Вид товара')
    description = models.TextField(blank=True, null=True, verbose_name='Описание товара')
    category = models.ManyToManyField(to='Category', verbose_name='Категории')
    tag = models.ManyToManyField(to='Tag', verbose_name='Теги')

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['product_name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Seller(models.Model):
    """Продавцы"""
    seller_name = models.CharField(max_length=20, null=False, unique=True, verbose_name='Наименование продавца')
    description = models.TextField(blank=True, null=True, verbose_name='Описание продавца')

    def __str__(self):
        return self.seller_name

    class Meta:
        ordering = ['seller_name']
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Price(models.Model):
    """Цены продавцов"""
    seller = models.ForeignKey(to='Seller', related_name='selling_objects', on_delete=models.CASCADE,
                                blank=False, null=False, verbose_name='Продавец')
    product = models.ForeignKey(to='Product', related_name='sellers', on_delete=models.CASCADE, blank=False,
                                null=False, verbose_name='Поставляемый товар')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    article = models.CharField(max_length=50, null=True, verbose_name='Артикул')
    comment = models.TextField(blank=True, null=True, verbose_name='Примечание')

    def __str__(self):
        return f'{self.product} поставляется {self.seller}'

    class Meta:
        verbose_name = "Цена продавца"
        verbose_name_plural = "Цены поставцов"
