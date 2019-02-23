from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User, Cart, CartProducts, Address
from ..products.models import Product

import bcrypt

# TODO: create the login functionality
# TODO: save the user id to the session when the user logs in
def register(request):
    if request.method == "GET":
        return render(request, 'user/register.html')
    if request.method == "POST":
        data = request.POST
        register_errors = User.objects.registration_validator(data)
        address_errors = Address.objects.address_validator(data)
        if len(register_errors) > 0 or len(address_errors) > 0:
            if register_errors:
                for key, value in register_errors.items():
                    messages.error(request, value)
            if address_errors:
                for key, value in address_errors.items():
                    messages.error(request, value)
            return redirect('/register')
        else:
            password = data['password'].encode()
            password = bcrypt.hashpw(password, bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], username=data['username'], password=password,phone_number=data['phone'])
            user.save()
            Address.objects.create(address_type=data['address_type'], address1=data['address_1'], city=data['city'], zip_code=data['zip_code'], state_province=data['state'], country=data['country'], user=user)
            request.session['user_id'] = user.id
            cart = Cart.objects.create(user=user)
            request.session['cart_id'] = cart.id
            return redirect('/')

def login(request):
    if request.method == "GET":
        return render(request, 'user/login.html')
    if request.method == "POST":
        data = request.POST
        errors = User.objects.login_validator(data)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        else:
            user = User.objects.get(username=data['username'])
            request.session['user_id'] = user.id
            return redirect('/')

def cart(request):
    if request.method == "GET":
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            cart = Cart.objects.get(user__id=user.id)
            cart_products = CartProducts.objects.filter(cart=cart)
            context = {
                'user': user,
                'cart_products': cart_products
            }
            return render(request, 'user/cart.html', context)
        else:
            return render(request, 'user/cart.html')

def add_to_cart(request, product_id, quantity):
    """ Add to Cart """
    # TODO: add functionality for a non registered or logged in user to add produdcts to their cart
    if request.method == "GET":
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.get(user__id=user.id)
            CartProducts.objects.create(amount=quantity, product=product, cart=cart)
            cart_products = CartProducts.objects.filter(cart__id = cart.id)
            print('*'*80)
            print(cart_products)
            for product in cart_products:
                print(product.product.images.all())
            context = {
                'user': user,
                'cart_products': cart_products
            }
            return redirect('/cart')
            # return render(request, 'user/cart.html', context)

def logout(request):
    if request.method == "GET":
        del request.session['user_id']
        return redirect('/')
