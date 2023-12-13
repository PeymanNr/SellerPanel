from django.db import models
from django.utils.translation import gettext as _


class Price(models.Model):
    created_time = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('created_time'))
    price = models.CharField(max_length=10, verbose_name=_('price'))

    class Meta:
        verbose_name = _('price')
        verbose_name_plural = _('prices')
        db_table = 'price'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    created_time = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('created_at'))
    description = models.TextField(verbose_name=_('description'))
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name=_('update_time'))
    price = models.ForeignKey(Price, on_delete=models.CASCADE,
                              related_name='products')

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        db_table = 'product'

    def __str__(self):
        return self.title
