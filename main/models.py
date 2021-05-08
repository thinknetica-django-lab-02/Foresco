from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms import MultipleChoiceField
from django.contrib.postgres.fields import ArrayField
from django.db.models import F

from django.contrib.auth.models import User


class Tag(models.Model):
    """Модель для хранения тегов"""
    tag = models.CharField(max_length=20, null=False, unique=True, verbose_name='Тег', help_text="Содержимое тэга")
    """Содержимое тэга"""
    description = models.TextField(blank=True, null=True, verbose_name='Описание тега', help_text="Описание тэга")

    def __str__(self):
        """Возвращает строкове представление тэга"""
        return self.tag + (f' ({self.description})' if self.description else '')

    @staticmethod
    def get_tag_list():
        """Получения списка тэгов для постановки"""
        return list(map(lambda x: (x['tag'], x['tag']), Tag.objects.all().values('tag')))

    class Meta:
        ordering = ['tag']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Category(models.Model):
    """Категории"""
    category_name = models.CharField(max_length=200, null=False, unique=True, verbose_name='Наименование категории',
                                     help_text="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name='Описание категории',
                                   help_text="Описание категории")

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name']
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class ChoiceArrayField(ArrayField):
    """Тип поля с функционалом выбора вариантов"""
    def formfield(self, **kwargs):
        defaults = {
            'form_class': MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class Product(models.Model):
    """Товары"""
    TYPECHOICES = (
        ('service', 'Услуга'),
        ('item', 'Предмет'),
    )
    """Варианты значений для поля Вид товара"""
    product_name = models.CharField(max_length=200, null=False, unique=True, verbose_name='Наименование товара',
                                    help_text="Название товара")
    product_type = models.CharField(max_length=7, null=False, default='item', choices=TYPECHOICES,
                                    verbose_name='Вид товара', help_text="Вид товара. Вибирается из вариантов")
    description = models.TextField(blank=True, null=True, verbose_name='Описание товара', help_text="Описание товара")
    category = models.ManyToManyField(to='Category', blank=True, verbose_name='Категории',
                                      help_text="Категории, к которым относится товар")
    tag = models.ManyToManyField(to='Tag', blank=True, related_name='products', verbose_name='Теги предыдущие')
    tags = ChoiceArrayField(base_field=models.CharField(max_length=20, choices=Tag.get_tag_list()), null=True,
                            verbose_name='Теги', help_text="Связанные с товаром тэги")
    certified = models.BooleanField(null=False, verbose_name='Требуется сертификат', default=False,
                                    help_text="Признак того, что товар нужно сертифицировать")
    product_image = models.ImageField(null=True, blank=True, verbose_name='Иллюстрация',
                                      help_text="Ссылка на иллюстрацию к товару")
    noticed = models.BooleanField(null=False, verbose_name='Разослан', default=False,
                                  help_text="Отметка о том, что товар был упомянут в рассылке о новинках")

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return "/products/%i/" % self.pk

    class Meta:
        ordering = ['product_name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Seller(models.Model):
    """Продавцы"""
    seller_name = models.CharField(max_length=20, null=False, unique=True, verbose_name='Наименование продавца',
                                   help_text="Наименование продавца")
    description = models.TextField(blank=True, null=True, verbose_name='Описание продавца',
                                   help_text="Описание продавца")

    def __str__(self):
        return self.seller_name

    class Meta:
        ordering = ['seller_name']
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Price(models.Model):
    """Цены продавцов"""
    seller = models.ForeignKey(to='Seller', related_name='selling_objects', on_delete=models.CASCADE,
                               blank=False, null=False, verbose_name='Продавец',
                               help_text="Продавец, установивший цену")
    product = models.ForeignKey(to='Product', related_name='sellers', on_delete=models.CASCADE, blank=False,
                                null=False, verbose_name='Поставляемый товар',
                                help_text="Товар, на который установлена цена")
    price = models.FloatField(null=True, blank=True, verbose_name='Цена',
                              help_text="Установленная продавцом цена на товар")
    article = models.CharField(max_length=50, null=True, verbose_name='Артикул', help_text="Артикул товара у продавца")
    comment = models.TextField(blank=True, null=True, verbose_name='Примечание', help_text="Примечание к цене")

    def __str__(self):
        return f'{self.product} поставляется {self.seller}'

    class Meta:
        verbose_name = "Цена продавца"
        verbose_name_plural = "Цены продавцов"


class Profile(models.Model):
    """Профили пользователей"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, verbose_name='Логин',
                                help_text="Ссылка на пользователя из станадартной модели Django")
    age = models.SmallIntegerField(null=True, blank=True, verbose_name='Возраст', help_text="Возраст пользователя")
    profile_image = models.ImageField(null=True, blank=True, verbose_name='Иллюстрация',
                                      help_text="Ссылка на иллюстрацию пользователя")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


class ViewCounter(models.Model):
    """Счетчик просмотров"""
    page_url = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name='Адрес страницы',
                                help_text="Просмотренный адрес")
    view_count = models.IntegerField(null=False, default=1, verbose_name='Количество просмотров',
                                     help_text="Количество просмотров")

    @staticmethod
    def count_view(page_url) -> None:
        """
        Инкремент просмотра
        :param page_url: Просматриваемый url
        :type page_url: строка до 255 символов
        """
        try:
            q = ViewCounter.objects.get(page_url=page_url)
            q.view_count = F('view_count') + 1
            q.save()
        except ObjectDoesNotExist:
            q = ViewCounter(page_url=page_url)
            q.save()

    @staticmethod
    def get_count(page_url: str) -> int:
        """
        Получение количества просмотров
        :param page_url: Просматриваемый url
        :type page_url: строка до 255 символов
        """
        try:
            q = ViewCounter.objects.get(page_url=page_url)
            return q.view_count
        except ObjectDoesNotExist:
            return 0

    class Meta:
        verbose_name = "Счетчик просмотров"
        verbose_name_plural = "Счетчики просмотров"
