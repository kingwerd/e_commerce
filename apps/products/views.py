from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Category, Product, ProductImages
from ..user.models import User, Review

# TODO: create a helper function to resize the images based on the template that they are currently in
# TODO: user the PIL module to help with this

def show_all_products(request):
    """ Details Hover """
    # TODO: when the user hovers over the image of a product, an overlay with information appears about the product
    """ Product Slider """
    # TODO: fix the size of the indicators that they are laid out horizontally instead of vertically
    # TODO: clean up the css file that is used for the product slider
    # TODO: update the layout for each product that is displayed
    # TODO: fix the prices to display the trailing 0
    if request.method == "GET":
        data = {}

        categories = Category.objects.all()

        for category in categories:
            length = len(category.products.all())
            data[f'{category.name}'] = []
            counter = 0
            product_arr = []
            for product in category.products.all():
                product_arr.append(product)
                counter += 1
                if counter % 4 == 0:
                    data[f'{category.name}'].append(product_arr)
                    product_arr = []
                elif counter == length:
                    data[f'{category.name}'].append(product_arr)
        context = {
            'data': data
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

def filter_products(request):
    """ Overall """
    # TODO: have different layouts for each type of filter
    # TODO: implement functionality to allow users to have multiple ratings at the same time
    # TODO: have all rating be executed with an ajax request that injects the partial html in the document
    """ Products Partial """
    # TODO: come up with a new layout for the partial when the user filters the products
    """ Categories """
    # TODO: update the category filter so that it has the new model representation
    """ Price """
    # TODO: create the double range slider so that the user can filter the products based on price
    # TODO: for the max price get the highest price and set the as the max for the range
    """ Ratings """
    # TODO: create the ratings filter that acts just like the rating buttons in the leave a review tab
    if request.method == "GET":
        data = request.GET
        category = None
        if data['category_filter']:
            if int(data['category_filter']) == 0:
                category = Category.objects.all()
            else:
                category = Category.objects.filter(id=int(data['category_filter']))
        elif data['price_filter']:
            print('getting products with a certain price')
        elif data['rating_filter']:
            print('getting products with a certain rating')
        context = {
            'categories': category
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
                for key, val in errors.items():
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