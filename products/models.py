from django.db import models

# Create your models here.
from categories.models import Category

class Product(models.Model):

    STYLE_CHOICES = (
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('streetwear', 'Streetwear'),
        ('sports', 'Sports'),
    )

    GENDER_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
    )

    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField( upload_to='products/')
    style_type = models.CharField(max_length=50,choices=STYLE_CHOICES)
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES)
    colour = models.CharField(max_length=50)
    tags = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
