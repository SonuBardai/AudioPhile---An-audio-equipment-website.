from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import UserPassesTestMixin

from shop.models import Item


def home(request):
    context = {
        'title': 'Home',
        'cart_items': 15
    }
    return render(request, 'shop/index.html', context)


class ShopItems(ListView):
    model = Item
    template_name = 'shop/shop_home.html'
    context_object_name = 'items'
    ordering = ['-date_listed']


class NewItem(UserPassesTestMixin, CreateView):
    model = Item
    fields = ['name', 'category', 'desc', 'price', 'stock', 'image']
    template_name = 'shop/item_form.html'

    def test_func(self):
        user = self.request.user
        return True if user.is_superuser else False

class EditItem(UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['name', 'category', 'desc', 'price', 'stock', 'image']
    template_name = 'shop/item_form.html'
    
    def test_func(self):
        user = self.request.user
        return True if user.is_superuser else False

class DeleteItem(UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/shop'

    def test_func(self):
        user = self.request.user
        return True if user.is_superuser else False