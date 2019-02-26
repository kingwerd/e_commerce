from django.db import models

import math

class CategoryManager(models.Manager):
    def category_validator(self, category_name):
        errors = {}
        if Category.objects.filter(name=category_name).exists():
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
    def average_product_rating(self, id):
        product = Product.objects.get(id=id)
        ratings = []
        for review in product.product_reviews.all():
            ratings.append(review.rating)
        return math.floor(sum(ratings) / len(ratings))

class Product(models.Model):
    name = models.CharField(max_length=155)
    price = models.FloatField()
    short_description = models.CharField(max_length=100)
    long_description = models.TextField()
    stock = models.IntegerField()
    average_rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    objects = ProductManager()

class ProductImages(models.Model):
    image = models.ImageField(upload_to='product/images', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

# class Clicks(models.Model):
#     times = models.IntegerField(default=0)
#     clicked_at = models.DateTimeField(auto_now_add=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="clicks")
#     users = models.ManyToManyField(User, related_name="clicks")