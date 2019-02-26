from django.urls import path
from . import views

# TODO: delete the product update route

urlpatterns = [
    path('', views.show_all_products),
    path('products/search/', views.product_search),
    path('products/filter/category', views.filter_categories),
    path('products/filter/price', views.filter_price),
    path('products/filter/rating', views.filter_rating),
    path('products/<int:id>', views.show_single_product),
    path('products/create', views.create_product),
    path('products/update/<int:id>', views.update_product),
    path('products/review/<int:id>', views.review_product),
    path('products/cart/modal', views.cart_modal),
]