from django.db import models

class CategoryManager(models.Manager):
    def category_validator(self, category_name):
        errors = {}
        if Category.objects.filter(name=name).exists():
            errors['cat_name_exists'] = "Category name already exists"
        return errors
    def create_category(self, category_name):
        Category.objects.create(name=category_name)

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CategoryManager()

class ProductManager(models.Manager):
    # TODO: get products within a certain price range
    # TODO: get products within a certain rating range

    def product_validator(self, post_data):
        errors = {}
        if len(post_data['product_name']) < 1:
            errors['product_name'] = 'Product name is required'
        if post_data['price'] < 0.0:
            errors['product_price'] = "Product price is required"
        if len(post_data['short_description']) < 1:
            errors['short_description'] = "Short description is required"
        if len(post_data['long_description']) < 1:
            errors['long_description'] = "Long description is required"
        if post_data['stock'] < 1:
            errors['stock'] = "Product must have an initial stock"
        if not post_data['category']:
            errors['product_category'] = "Product must have a cateogry"
        return errors
    def create_product(self, name, price, short, long, stock, category_id):
        product = Product.objects.create(name=name, price=price, short_description=short, long_description=long, stock=stock, category=Category.objects.get(id=category_id))
    def get_products_in_category(self, category_id):
        products = Product.objects.filter(category__id=category_id)
        return products

class Product(models.Model):
    # TODO: get rid of the image field for the product that is currently being used
    # TODO: update the template loops to display the correct path to the new model relationship
    # TODO: update the view so that they are saving an instance of the products with its related images
    # TODO: change the file upload for wherever there is a file to be uploaded to multiple
    # TODO: see what data is returned from a multiple file upload and work from there
    name = models.CharField(max_length=155)
    price = models.FloatField()
    short_description = models.CharField(max_length=100)
    long_description = models.TextField()
    stock = models.IntegerField()
    """ image field will eventually be replaced by the one to many relationship with ProductImages  """
    # main_image = models.ImageField(upload_to='products/images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    objects = ProductManager()
"""
Since there is not a model field to handle multiple file uploads I have created another
model that will hold the image and the product that the image is related to.
"""
class ProductImages(models.Model):
    # TODO: figure out how to link a product with multiple images
    # TODO: determine where to store each image if it is not in a separate file
    image = models.ImageField(upload_to='product/images', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")