from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class Item(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)
    desc = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField(default=10)
    rating = models.IntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    image = models.ImageField(upload_to="item_pics")
    date_listed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}, {self.category}'

    def get_absolute_url(self):
        return reverse('home')
    
    def save(self):
        self.slug = slugify(self.name)
        super().save()