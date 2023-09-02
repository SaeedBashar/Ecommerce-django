from django.urls import path
from . import views

urlpatterns = [

        path('', views.store, name="store"),
        path('cart/', views.cart, name="cart"),
        path('checkout/', views.checkout, name="checkout"),
        path('update_item/', views.updateItem, name="update_item"),
        path('process_order/', views.processOrder, name="process_order"),
        path('product/<int:id>', views.product_detail, name="product"),
        path('process_momo', views.processMomo, name="momo"),
        path('verify_momo_tx/<ref>', views.verifyMomoTX, name="momoverify")
]