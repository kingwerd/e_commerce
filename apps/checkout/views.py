from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import BillingInformation, ShippingInformation, PaymentInformation, Order
from ..user.models import User, Cart, Address, CartProducts

"""
TODO: test the checkout system for any bugs that may occur
TODO: determine where the creation of an order should take place
TODO: when the user completes an order delete all the items in their cart
TODO: add functionality for a non logged in user to make orders and add items to their cart
TODO: when the user makes an order subtract the quantity purchased for each product
"""

def checkout(request):
    if request.method == "GET":
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            cart = Cart.objects.get(user=user)
            cart_products = CartProducts.objects.filter(cart=cart)
            total = 0
            for product in cart_products:
                total += product.product.price * product.amount
            if Order.objects.filter(cart=cart).exists():
                Order.objects.get(cart=cart).delete()
            order = Order.objects.create(total=total, cart=cart, user=user)
            request.session['order_id'] = order.id
            request.session['cart_id'] = cart.id
            context = {
                'user': user,
                'cart': cart,
                'cart_products': cart_products,
                'total': total
            }
            return render(request, 'checkout/checkout.html', context)
        else:
            # if there is no user id currently in session that it is a user who is not
            # a memeber of the service
            pass

def billing_information(request):
    if request.method == "POST":
        data = request.POST
        order_id = request.session['order_id']
        if 'user_id' in request.session and 'cart_id' in request.session:
            order = Order.objects.get(cart__id=request.session['cart_id'])
            bill_address_errors = Address.objects.address_validator(data)
            if bill_address_errors > 0:
                for key, value in bill_address_errors.items():
                    messages.error(request, value)
                    return redirect('/checkout')
            else:
                bill_info_errors = BillingInformation.objects.billing_info_validator(data)
                if bill_info_errors > 0:
                    for key, value in bill_info_errors.items():
                        messages.error(request, value)
                        return redirect('/checkout')
                else:
                    address = Address.objects.create(address1=data['billing-address'], city=data['billing-town-city'], zip_code=data['billing-zip-postal'], state_province=data['billing-state'])
                    bill_info = BillingInformation.objects.create(first_name=data['billing-first-name'], last_name=data['billing-last-name'], email=data['billing-email-address'], phone=data['billing-phone'], address=address)

def shipping_information(request):
    if request.method == "POST":
        data = request.POST
        order_id = request.session['order_id']
        if 'user_id' in request.session and 'cart_id' in request.session:
            order = Order.objects.get(cart__id=request.session['cart_id'])
            ship_info_errors = ShippingInformation.objects.shipping_info_validator(data)
            if ship_info_errors > 0:
                for key, value in ship_info_errors.items():
                    messages.error(request, value)
                    return redirect('/checkout')
            else:
                address = Address.objects.create(address1=data['new-adr-address'], city=data['new-adr-town-city'], zip_code=data['new-adr-zip-postal'], state_province=data['new-adr-state'])
                ship_info = ShippingInformation.objects.create(first_name=data['new-adr-first-name'], last_name=data['new-adr-last-name'], email=data['new-adr-email-address'], phone=data['new-adr-phone'], shipment_method=data['shipping_options'])

def payment_information(request):
    if request.method == "POST":
        data = request.POST
        order_id = request.session['order_id']
        if 'user_id' in request.session and 'cart_id' in request.session:
            order = Order.objects.get(cart__id=request.session['cart_id'])
            pay_info_errors = PaymentInformation.objects.payment_information_validator(data)
            if pay_info_errors > 0:
                for key, value in pay_info_errors.items():
                    messages.error(request, value)
                    return redirect('/checkout')
            else:
                pay_info = PaymentInformation.objects.create(payment_method=data['payment_method'])