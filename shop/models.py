from turtle import ondrag
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


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
        return f'{self.id}, {self.name}'

    def get_absolute_url(self):
        return reverse('home')

    def save(self):
        self.slug = slugify(self.name)
        super().save()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    placed = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'Order of {self.user.username}, ordered on: {self.date_ordered.strftime("%d-%m-%y")}, status: {self.delivered}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order_ID: {self.order.id}, Item_ID: {self.item.id}, Q: {self.quantity}'
