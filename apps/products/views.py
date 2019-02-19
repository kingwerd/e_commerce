from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Category, Product, ProductImages

# TODO: create a helper function to resize the images based on the template that they are currently in
# TODO: user the PIL module to help with this

def show_all_products(request):
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
                elif counter == length-1:
                    data[f'{category.name}'].append(product_arr)
        context = {
            'data': data
        }
        return render(request, 'products/show_products.html', context)

# TODO: images so that they are rendering based on the amount of images the product has
def show_single_product(request, id):
    if request.method == "GET":
        product = Product.objects.get(id=id)
        context = {
            'product': product,
            'rating': 4
        }
        return render(request, 'products/product.html', context)

# TODO: render the search options in the datalist and set a max height of the view
def product_search(request):
    if request.method == "GET":
        search_string = list(request.GET.keys())[0]
        data = Product.objects.filter(name__startswith=search_string)
        names = []
        for obj in data:
            names.append(obj.name)
        return JsonResponse(names, safe=False)

# TODO: create the price min and max filter 
# TODO: create the product ratings filter
def filter_products(request):
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

# TODO: update the function so that it can handle the new multiple file model ProductImages
# TODO: do the same thing for the create_production function
def update_product(request, id):
    if request.method == "GET":
        return render(request, 'products/edit_product.html', {'product': Product.objects.get(id=id)})
    if request.method == "POST":
        product_images = request.FILES.getlist('product_images')
        product = Product.objects.get(id=id)
        for image in product_images:
            ProductImages.objects.create(image=image, product=product)
        product.save()
        return redirect('/')