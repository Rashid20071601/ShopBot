from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)
    category = models.CharField(max_length=150, verbose_name='Категория')

    def __str__(self):  # __str__ для отображения в админке, __unicode__ для отображения в браузере
        return self.name