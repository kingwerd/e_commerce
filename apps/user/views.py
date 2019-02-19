from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User, Cart
from ..products.models import Product

import bcrypt

# TODO: create the login functionality
# TODO: save the user id to the session when the user logs in
def register(request):
    if request.method == "GET":
        return render(request, 'user/register.html')
    if request.method == "POST":
        data = request.POST
        errors = User.objects.registration_validator(data)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            password = data['password'].encode()
            password = bcrypt.hashpw(password, bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], username=data['username'], password=password,phone_number=data['phone'])
            user.save()
            request.session['user_id'] = user.id
            Cart.objects.create(user=user)
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
            context = {
                'user': user,
                'cart': cart
            }
            return render(request, 'user/cart.html', context)
        else:
            return render(request, 'user/cart.html')

def add_to_cart(request, id):
    if request.method == "GET":
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            product = Product.objects.get(id=id)
            cart = Cart.objects.get(user__id=user.id)
            cart.products.add(product)
            product.carts.add(cart)
            product.save()
            cart.save()
            context = {
                'user': user,
                'cart': cart
            }
            return render(request, 'user/cart.html', context)


def logout(request):
    if request.method == "GET":
        del request.session['user_id']
        return redirect('/')
