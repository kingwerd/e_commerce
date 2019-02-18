from django.urls import path
from . import views

# TODO: create the register login path
# TODO: create the review path for when a user makes a review on a product

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('cart', views.cart),
    path('cart/add/<int:id>', views.add_to_cart),
    path('logout', views.logout)
]