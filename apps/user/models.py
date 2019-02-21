from django.db import models
from ..products.models import Product

import re
import bcrypt

# TODO: create the user model with the appropriate fields
# TODO: create the user model manager with the appropriate functions

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 1:
            errors['first_name'] = "First name is required!"
        if len(post_data['last_name']) < 1:
            errors['last_name'] = "Last name is required!"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email!"
        if len(post_data['password']) < 7:
            errors['password'] = "Password must be at least 8 characters"
        if len(post_data['phone']) != 10:
            errors['phone'] = "Phone number is required and must be 10 numbers"
        if post_data['password'] != post_data['confirm_pw']:
            errors['confirm_pw'] = "Passwords do not match"
        return errors
    def username_check(self, username):
        if User.objects.filter(username=username).exists():
            return True
        else:
            return False
    def email_check(self, email):
        if User.objects.filter(email=email).exists():
            return True
        else:
            return False
    def login_validator(self, post_data):
        errors = {}
        if len(post_data['username']) < 1:
            errors['username_field'] = "Username is required"
        if len(post_data['password']) < 1:
            errors['password_field'] = "Password is required"
        if not User.objects.filter(username=post_data['username']).exists():
            errors['username_exists'] = "Username does not exist"
        else:
            user = User.objects.get(username=post_data['username'])
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = f"Password for {post_data['username']} is incorrect"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class AddressManager(models.Manager):
    def address_validator(self, post_data):
        STREET_ADDRESS_REGEX = re.compile('\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', re.IGNORECASE)
        errors = {}
        # if post_data['address_type'] != 1 or post_data['address_type'] != 2:
        #     errors['address_type'] = "Address type is required"
        if not post_data['address_type']:
            errors['address_type'] = "Address type is required"
        if len(post_data['address_1']) < 1:
            errors['address_1'] = "Street number is required"
        if not STREET_ADDRESS_REGEX.match(post_data['address_1']):
            errors['address_1_format'] = "Incorrect address format"
        if not post_data['city']:
            errors['city'] = "City is required"
        if len(post_data['zip_code']) != 5:
            errors['zip_code'] = "Zip code is required and must be 5 numbers"
        if not post_data['state']:
            errors['state'] = "State  is required"
        if not post_data['country']:
            errors['country'] = "Country is required"
        return errors

# TODO: create the address model with the appropriate fields
class Address(models.Model):
    address_type = models.IntegerField()
    address1 = models.CharField(max_length=255, default="")
    address2 = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=150)
    zip_code = models.IntegerField()
    state_province = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    objects = AddressManager()

class ReviewManager(models.Manager):
    def review_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 1:
            errors['title'] = "Title is required"
        if len(post_data['review']) < 10:
            errors['review'] = "Review must be more than 10 characters"
        if not post_data['rating']:
            errors['rating'] = "Rating is required"
        return errors

# TODO: create the review model with the appropriate fields
class Review(models.Model):
    title = models.CharField(max_length=150)
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_reviews")
    objects = ReviewManager()

class CartManager(models.Manager):
    """ Used to make sure that the user does not add the same product to their cart """
    def cart_validator(self, user_id, product):
        errors = {}
        cart = Cart.objects.get(user__id=user_id)
        if product in cart.products.all:
            errors['duplicate_product'] = "You already have this item in your cart"
        return errors

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")

class CartProducts(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_products")
