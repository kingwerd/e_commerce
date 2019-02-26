from django.db import models
from ..products.models import Product
from ..user.models import User, Address, Cart

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
STREET_ADDRESS_REGEX = re.compile('\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', re.IGNORECASE)
VISA_REGEX = re.compile(r'^4[0-9]{12}(?:[0-9]{3})?$')
MASTER_CARD_REGEX = re.compile(r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$')
DISCOVER_REGEX = re.compile(r'^6(?:011|5[0-9]{2})[0-9]{12}$')
EXPIRATION_DATE_REGEX = re.compile(r'^0[1-9]|^(11)|^(12)[0-9][0-9]$')

class BillingInformationManager(models.Manager):
    def billing_info_validator(self, post_data):
        errors = {}
        if len(post_data['billing-first-name']) < 1:
            errors['billing-first-name'] = "First name for the bill is required"
        if len(post_data['billing-last-name']) < 1:
            errors['billing-last-name'] = "Last name for the bill is required"
        if not EMAIL_REGEX.match(post_data['billing-email-address']):
            errors['billing-email-address'] = "Invalid email address format"
        if len(post_data['billing-phone']) != 10:
            errors['billing-phone'] = "Phone number must be 10 numbers"
        if not STREET_ADDRESS_REGEX.match(post_data['billing-address']):
            errors['billing-address'] = "Not a valid address"
        if not post_data['billing-town-city'] or len(post_data['billing-town-city']) < 1:
            errors['billing-town-city'] = "City is required"
        if not post_data['billing-state'] or len(post_data['billing-state']) < 1:
            errors['billing-state'] = "State is required"
        if not post_data['billing-zip-postal'] or len(post_data['billing-zip-postal']) != 5:
            errors['billing-zip-postal'] = "Zip code is required"
        return errors

class BillingInformation(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='bill_addresses')
    objects = BillingInformationManager()

class ShippingInformationManager(models.Manager):
    def shipping_info_validator(self, post_data):
        errors = {}
        if not post_data['shipping_options']:
            errors['shipping_options'] = "You must choose a shipping option"
        return errors
    def new_shipping_address_validator(self, post_data):
        errors = {}
        if STREET_ADDRESS_REGEX.match(post_data['new-adr-address']):
            errors['new-adr-address'] = "Invalid address format"
        if post_data['new-adr-town-city'] < 1:
            errors['new-adr-town-city'] = "City is required"
        if post_data['new-adr-state'] < 1:
            errors['new-adr-state'] = "State is required"
        if post_data['new-adr-zip-postal'] < 1:
            errors['new-adr-zip-postal'] = "Zip code is required"
        return errors

class ShippingInformation(models.Model):
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=10, default="")
    shipment_method = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='ship_addresses')
    objects = ShippingInformationManager()

class PaymentInformationManager(models.Manager):
    def payment_information_validator(self, post_data):
        errors = {}
        if post_data['billing_options'] == 2:
            if VISA_REGEX.match(post_data['card-number']):
                pass
            elif MASTER_CARD_REGEX.match(post_data['card-number']):
                pass
            elif DISCOVER_REGEX.match(post_data['card-number']):
                pass
            else:
                errors['card-number'] = "Invalid or not a supported card number"
            if post_data['card-name-on'] < 1:
                errors['card-name-on'] = "Name for card is required"
            if EXPIRATION_DATE_REGEX.match(post_data['card-expiration-date']):
                errors['card-expiration-date'] = "Invalid expiration date"
            if post_data['card-cvv'] != 3:
                errors['card-cvv'] = "Invalid card CVV"
        return errors

class PaymentInformation(models.Model):
    payment_method = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PaymentInformationManager()

class Order(models.Model):
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='orders', default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', default=None)
    billing_info = models.ForeignKey(BillingInformation, on_delete=models.CASCADE, related_name='orders', default=None)
    shipping_info = models.ForeignKey(ShippingInformation, on_delete=models.CASCADE, related_name='orders', default=None)
    payment_info = models.ForeignKey(PaymentInformation, on_delete=models.CASCADE, related_name='orders', default=None)
