from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse, Http404
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder
from .momo_pay import PayClass

def index(request):
    return render(request, 'store/index.html')

def store(request):
    
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

@login_required
def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

@login_required
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

@login_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@login_required
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

@login_required
def product_detail(request, id):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    product = Product.objects.get(id=id)
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'product': product}
    return render(request, 'store/product_detail.html', context)

@login_required
def processMomo(request):
    if request.method == "POST":
        body = json.loads(request.body)
        try:
            res = PayClass.momopay(
                body["amount"], "EUR", 
                "afrimart_purchase", 
                "233" + body["phone"][1:], body["msg"])
            print(res)
            if(res["response"] == 200 or res["response"] == 201 or res["response"] == 202):
                return JsonResponse({"status": True, "msg": "Transaction Processed", "ref": res["ref"]})
            else:
                return JsonResponse({"status": False, "msg": "Failed To Process Transaction"})
                
        except:
            return JsonResponse({"status": False, "msg": "An error Occured While Processing"})
        
    else:
        return JsonResponse({"status": False, "msg": "No Data To Process"})
    
@login_required
def verifyMomoTX(request, ref):
    res = PayClass.verifymomo(ref)
    if res["status"] == "SUCCESSFUL":
        return JsonResponse({"status": True, "msg": "Thank you for buying this item"})
    else:
        return JsonResponse({"status": False, "msg": "Transaction not approved"})

        