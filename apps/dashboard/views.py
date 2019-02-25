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
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'dashboard/dashboard.html', context)
    # if not 'user_id' in request.session:
    #     return redirect('/')
    # else:        
    #     pass