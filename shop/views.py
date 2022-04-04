from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import UserPassesTestMixin

from shop.models import Item, Order, OrderItem


def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'shop/index.html', context)


def createCart(request):
    items = Item.objects.all()
    cart = dict()
    user = request.user
    order, created = Order.objects.get_or_create(user=user, placed=False)
    orderItems = order.orderitem_set.all()
    for item in orderItems.values_list('item_id', 'quantity'):
        cart[item[0]] = item[1]
    for item in items:
        if not cart.get(item.id):
            cart[item.id] = 0
    return cart


class ShopItems(ListView):
    model = Item
    template_name = 'shop/shop_home.html'
    context_object_name = 'items'
    ordering = ['-date_listed']

    def get_context_data(self, *args, **kwargs):
        context = super(ShopItems, self).get_context_data(*args, **kwargs)
        context['cart'] = json.dumps(createCart(self.request))
        return context


class DetailItem(DetailView):
    model = Item

    def get_context_data(self, *args, **kwargs):
        context = super(DetailItem, self).get_context_data(*args, **kwargs)
        context['cart'] = json.dumps(createCart(self.request))
        return context


class NewItem(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Item
    fields = ['name', 'category', 'desc', 'price', 'stock', 'image']
    template_name = 'shop/item_form.html'

    def test_func(self):
        user = self.request.user
        return True if user.is_superuser else False


class EditItem(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['name', 'category', 'desc', 'price', 'stock', 'image']
    template_name = 'shop/item_form.html'

    def test_func(self):
        user = self.request.user
        return True if user.is_superuser else False


class DeleteItem(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/shop'

    def test_func(self):
        user = self.request.user
        return True if user.is_superuser else False


def cart(request):
    order, created = Order.objects.get_or_create(user=request.user)
    items = order.orderitem_set.all()

    cart = createCart(request)

    return render(request, 'shop/cart.html', {'items': items, 'cart': cart})


def updateCart(request):
    if request.method == 'POST':
        content = json.loads(request.body)
        id, action = content.get('id'), content.get('action')

        item = Item.objects.get(id=id)

        order, created = Order.objects.get_or_create(
            user=request.user, placed=False)

        orderItem, created = OrderItem.objects.get_or_create(
            order=order, item=item)
        if action == 'inc':
            orderItem.quantity += 1
        else:
            if orderItem.quantity <= 0:
                orderItem.quantity = 0
            else:
                orderItem.quantity -= 1
        orderItem.save()
    return JsonResponse(f'{orderItem.item.id}: {orderItem.quantity}', safe=False)


def checkout(request):
    return render(request, 'shop/checkout.html')
