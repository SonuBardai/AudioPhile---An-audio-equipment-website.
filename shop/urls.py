from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/category/<str:category>', views.ShopItems.as_view(), name='shop'),
    path('shop/new', views.NewItem.as_view(), name='new-item'),
    path('shop/edit/<str:slug>', views.EditItem.as_view(), name='edit-item'),
    path('shop/delete/<str:slug>', views.DeleteItem.as_view(), name='delete-item'),
    path('shop/item/<str:slug>', views.DetailItem.as_view(), name='detail-item'),
    path('shop/cart', views.cart, name='cart'),
    path('update_cart', views.updateCart, name="update_cart"),
    path('checkout', views.checkout, name="checkout"),
]