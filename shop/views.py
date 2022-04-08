from django.shortcuts import render, redirect
from django.contrib import messages
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

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import UserPassesTestMixin

from shop.models import Item, Order, OrderItem, ShippingAddress

from .forms import ShippingAddressForm


def createCart(request):
    items = Item.objects.all()
    cart = dict()
    user = request.user
    order = Order.objects.filter(user=user, placed=False).first()
    if order:
        orderItems = OrderItem.objects.filter(order = order)
        if orderItems:
            for item in orderItems.values_list('item_id', 'quantity'):
                cart[item[0]] = item[1]
            for item in items:
                if not cart.get(item.id):
                    cart[item.id] = 0
        else:
            for item in items:
                OrderItem.objects.create(order=order, item=item)
                cart[item.id] = 0
    return cart


def home(request):
    context = {
        'title': 'Home',
        'cart': createCart(request) if request.user.is_authenticated else None
    }
    return render(request, 'shop/index.html', context)


class ShopItems(ListView):
    model = Item
    template_name = 'shop/shop_home.html'
    context_object_name = 'items'
    ordering = ['-date_listed']

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = super(ShopItems, self).get_context_data(*args, **kwargs)
            context['cart'] = json.dumps(createCart(self.request))
            return context
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self):
        cat = self.kwargs['category']
        return super().get_queryset().filter(category=cat)


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


@login_required
def cart(request):
    try:
        order = Order.objects.get(user=request.user)
        items = order.orderitem_set.all()
    except Order.DoesNotExist:
        order = Order.objects.create(user=request.user)
        items = []

    subTotal = order.orderTotal

    cart = createCart(request)

    return render(request, 'shop/cart.html', {
        'items': items,
        'cart': cart,
        'subTotal': subTotal
    })


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

        orderItem.orderItemTotal = orderItem.quantity * orderItem.item.price

        orderItem.save()

        orderItems = order.orderitem_set.all()
        total = 0
        for i in orderItems:
            total += (i.quantity * i.item.price)

        order.orderTotal = total
        order.save()

    return JsonResponse(f'{orderItem.item.id}: {orderItem.quantity}', safe=False)


@login_required
def checkout(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Order Placed")
            return redirect('/')
    else:
        address = ShippingAddress.objects.filter(user=request.user).first()

        order, created = Order.objects.get_or_create(user=request.user)
        subTotal = order.orderTotal

        items = order.orderitem_set.all()

        cart = createCart(request)

        if address:
            form = ShippingAddressForm(instance=address)
        else:
            form = ShippingAddressForm()

        return render(request, 'shop/checkout.html', {'form': form, 'items': items, 'subTotal': subTotal})
