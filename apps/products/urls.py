from django.urls import path
from . import views

# TODO: delete the product update route

urlpatterns = [
    path('', views.show_all_products),
    path('products/search/', views.product_search),
    path('products/filter', views.filter_products),
    path('products/<int:id>', views.show_single_product),
    path('products/create', views.create_product),
    path('products/update/<int:id>', views.update_product)
]