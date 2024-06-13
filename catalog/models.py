from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save 

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='static\image', null=True, blank=True, default='static/image/333.jpg')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        db_table = 'Category'
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("cat_s", kwargs={"cat_slug": self.slug})
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=10, verbose_name='Категория')
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название товара', unique=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='static\image', null=True, blank=True, default='static/image/333.jpg')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Количество на складе')
    available = models.BooleanField(default=True)
    hit = models.BooleanField(default=False)
    discount = models.IntegerField(default=0, verbose_name='Размер скидки, %')
    discounted_price = models.IntegerField(null=True, verbose_name='Размер скидки, руб')
    sell_price = models.IntegerField(null=True, verbose_name='Цена со скидкой')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обнавления')

    class Meta:
        db_table = 'Product' # Читабельное имя таблицы в БД
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        #ordering = ('name',)
    
    def __str__(self):
        return self.name
 
    def get_absolute_url(self):
        return reverse("prod", kwargs={"prod_slug": self.slug})
    
    @property
    def discounted_price(self):
        return round(((self.price)*(self.discount))/100,2)

    @property
    def sell_price(self):
        return (self.price)-(self.discounted_price)
    
@receiver(post_save, sender=Product)
def update_available(sender, instance, **kwargs):
    if instance.stock == 0 and instance.available:
        instance.available = False
        instance.save()
    elif instance.stock > 0 and not instance.available:
        instance.available = True
        instance.save()
    
