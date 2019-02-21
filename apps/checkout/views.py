from django.shortcuts import render
from django.http import HttpResponse

def checkout(request):
    if request.method == "GET":
        if 'user_id' in request.session:
            # TODO: get the address(es) that are associated with the user
            # TODO: if the user does not have an address then prompt them to create one
            # TODO: populate the fields with the correct information for the user
            # TODO: get the cart and the products that are in it
            # TODO: populate the order summary table with the prices, products, and grand total 
            pass
        return render(request, 'checkout/checkout.html')