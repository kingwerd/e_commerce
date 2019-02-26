from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Category, Product, ProductImages
from ..user.models import User, Review, Address, Cart, CartProducts
from ..checkout.models import BillingInformation, ShippingInformation, PaymentInformation, Order
import bcrypt
import math
import random
"""
TODO: add the links to the single product page
TODO: add 'add to cart' and 'checkout' buttons to the cart
TODO: create a popup notification when the user adds a product to their account
TODO: create a bootstrap badge for the cart button that shows how many products that are in a users cart
TODO: update the navbar for the single product page with the correct links
"""
#1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,  30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50
# user id's range: 7 - 208
def show_all_products(request):
    # for product in Product.objects.all():
    #     product.average_rating = Product.objects.average_product_rating(product.id)
    #     product.save()
    # for rev in Review.objects.all():
    #     rev.rating = random.randint(1,5)
    #     rev.save()
    # for user in User.objects.all():
    #     cart = Cart.objects.get(user__id=user.id)
    #     rand_loop_var = random.randint(1,7)
    #     rand_prod_ids = []
    #     for i in range(rand_loop_var):
    #         ran_prod_id = random.randint(1,50)
    #         rand_prod_ids.append(ran_prod_id)
    #         idx = 0
    #         while (ran_prod_id == rand_prod_ids[idx]):
    #             ran_prod_id = random.randint(1,50)
    #             idx += 1
    #             if idx == len(rand_prod_ids):
    #                 break
    #     for p_id in rand_prod_ids:
    #         product = Product.objects.get(id=p_id)
    #         rand_amt = random.randint(1,8)
    #         CartProducts.objects.create(amount=rand_amt, product=product, cart=cart)
    #     total = 0
    #     cart_products = CartProducts.objects.filter(cart__id=cart.id)
    #     for product in cart_products:
    #         total += product.product.price * product.amount
    #     address = Address.objects.filter(user__id=user.id)[0]
    #     bill_info = BillingInformation.objects.create(first_name=user.first_name, last_name=user.last_name, email=user.email, phone=user.phone_number, address=address)
    #     bill_info.save()
    #     ship_info = ShippingInformation.objects.create(first_name=user.first_name, last_name=user.last_name, email=user.email, phone=user.phone_number, shipment_method=1, address=address)
    #     ship_info.save()
    #     pay_info = PaymentInformation.objects.create(payment_method=2)
    #     pay_info.save()
    #     order = Order.objects.create(total=total, cart=cart, user=user, billing_info=bill_info, shipping_info=ship_info, payment_info=pay_info)
    #     order.save()
    #     for p in cart_products:
    #         p.delete()

    
    """ Details Hover """
    # TODO: when the user hovers over the image of a product, an overlay with information appears about the product
    """ Product Slider """
    # TODO: fix the size of the indicators that they are laid out horizontally instead of vertically
    # TODO: clean up the css file that is used for the product slider
    # TODO: update the layout for each product that is displayed
    # TODO: fix the prices to display the trailing 0
    if request.method == "GET":
        data = {}
        max_price = 0
        categories = Category.objects.all()
        status = False
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            if user.status == 2:
                status = True
        for category in categories:
            length = len(category.products.all())
            data[f'{category.name}'] = []
            counter = 0
            product_arr = []
            for product in category.products.all():
                if product.price > max_price:
                    max_price = product.price
                product_arr.append(product)
                counter += 1
                if counter % 4 == 0:
                    data[f'{category.name}'].append(product_arr)
                    product_arr = []
                elif counter == length:
                    data[f'{category.name}'].append(product_arr)
        context = {
            'categories': categories,
            'max_price': max_price,
            'data': data,
            'status': status
        }
        return render(request, 'products/show_products.html', context)

def show_single_product(request, id):
    """ Information """
    # TODO: change the style, color, and font of the product name to stand out more
    # TODO: have the numeric representation of the reviews and star reviews evenly posititioned next to each other
    # TODO: change the style, color, and font of the description header
    # TODO: change the style, color, and font of the description so it looks like it is in its own box
    # TODO: add the buy now button and add to cart button to the page around or near the quantity drop down
    """ Images """
    # TODO: update the layout of the images so there is a single box that is holding the main image
    # TODO: when the user hovers over an image change the main image being displayed to the current image being hovered over
    # TODO: if the users mouse goes off of the image then it reverts back to the original main image
    # TODO: if the user clicks on the image they are hovering over it will be displayed as the main image
    """ Reviews """
    # TODO: update the layout for each review so the profile pic, user name, rating, title, and review and visually pleasing
    # TODO: add filters for the reviews tab so the user can sift through the reviews
    # TODO: change the rating stars that that the stars that are not checked are gray
    # TODO: change the notification incase there is no reviews for a product
    """ Leave a Review """
    # TODO: change the layout of the leave a review so that it ressizes and does not change the overall layout of the page 
    if request.method == "GET":
        product = Product.objects.get(id=id)
        average_rating = Product.objects.average_product_rating(id)
        context = {
            'product': product,
            'rating': average_rating
        }
        return render(request, 'products/product.html', context)

# TODO: render the search options in the datalist and set a max height of the view
def product_search(request):
    """ Search Bar """
    # TODO: add the datalist so that it displays the products that contain the characters that are entered into the search bar
    # TODO: make sure that the datalist does not go past a certain height and is scrollable
    if request.method == "GET":
        search_string = list(request.GET.keys())[0]
        data = Product.objects.filter(name__startswith=search_string)
        names = []
        for obj in data:
            names.append(obj.name)
        return JsonResponse(names, safe=False)

"""
##################################################################################################################
FILTERS
    ## Overall ##
    TODO: have different layouts for each type of filter
    TODO: implement functionality to allow users to have multiple ratings at the same time
    TODO: have all rating be executed with an ajax request that injects the partial html in the document
    ## Products Partial ##
    TODO: come up with a new layout for the partial when the user filters the products
    ## Categories ##
    TODO: update the category filter so that it has the new model representation
    ## Ratings ##
    TODO: create the ratings filter that acts just like the rating buttons in the leave a review tab
##################################################################################################################
"""
def filter_price(request):
    if request.method == "GET":
        min_price = int(request.GET['min-price-slider'])
        max_price = int(request.GET['max-price-slider'])
        products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
        # products.order_by('price').asc()
        context = {
            'products': products,
            'min': min_price,
            'max': max_price 
        }
        return render(request, 'products/_products.html', context)
def filter_categories(request):
    if request.method == "GET":
        data = request.GET
        category = None
        if data['category_filter']:
            if int(data['category_filter']) == 0:
                category = Category.objects.all()
            else:
                category = Category.objects.filter(id=int(data['category_filter']))
        context = {
            'categories': category
        }
        return render(request, 'products/_products.html', context)

def filter_rating(request):
    if request.method == "GET":
        data = request.GET
        products = Product.objects.filter(average_rating__gte=float(data['rating']))
        context = {
            'rating': data['rating'],
            'products': products
        }
        return render(request, 'products/_products.html', context)

# TODO: update the input file field to handle multiple files
# TODO: create a loop to filter out each file that is returned from the post request
def create_product(request):
    if request.method == "GET":
        return render(request, 'products/create_product.html', {'categories': Category.objects.all()})
    if request.method == "POST":
        # only do file upload with the update method
        # only accept one image at once
        data = request.POST
        return redirect('/')

def update_product(request, id):
    if request.method == "GET":
        return render(request, 'products/edit_product.html', {'product': Product.objects.get(id=id)})
    if request.method == "POST":
        product_images = request.FILES.getlist('product_images')
        product = Product.objects.get(id=id)
        if request.POST['product_name']:
            product.name = request.POST['product_name']
        for image in product_images:
            ProductImages.objects.create(image=image, product=product)
        product.save()
        return redirect('/')

def review_product(request, id):
    if request.method == "POST":
        if 'user_id' in request.session:
            data = request.POST
            errors = Review.objects.review_validator(data)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/products/{id}')
            else:
                review = Review.objects.create(title=data['title'], comment=data['review'], rating=int(data['rating']), user=User.objects.get(id=request.session['user_id']), product=Product.objects.get(id=id))
                review.save()
                return redirect(f'/products/{id}')

def cart_modal(request):
    # TODO: change the design of the add to cart modal so that it is more visually pleasing
    if request.method == "GET":
        data = request.GET['product']
        context = {
            'product': Product.objects.get(id=int(data))
        }
        print(data)
        return render(request, 'products/_cart_modal.html', context)