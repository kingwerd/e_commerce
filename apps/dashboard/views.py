from django.shortcuts import render, redirect

from ..user.models import *
from ..products.models import *
from ..checkout.models import *

"""
TODO: add checks to make sure that the client requesting the route is a logged in user AND an admin
TODO: transfer the 'create product' and 'edit product' to this application
TODO: use mockaroo for fake data for users, reviews, and orders
TODO: add an analytics page that shows visualizations of the data of the products
TODO: add a page for the admin to see all the users and the information
TODO: add a page to see all of a user's information
TODO: add a page to see a single review and be able to edit the review
"""

def dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        if user.status == 2:
            categories = Category.objects.all()
            context = {
                'categories': categories
            }
            return render(request, 'dashboard/dashboard.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def users(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        if user.status == 2:
            users = User.objects.all()
            context = {
                'users': users
            }
            return render(request, 'dashboard/users.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def products(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        if user.status == 2:
            categories = Category.objects.all()
            context = {
                'categories': categories
            }
            return render(request, 'dashboard/dashboard.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def orders(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        if user.status == 2:
            orders = Order.objects.all()
            context = {
                'orders': orders
            }
            return render(request, 'dashboard/orders.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')
