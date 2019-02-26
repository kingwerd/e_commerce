from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard),
    path('dashboard/users', views.users),
    path('dashboard/products', views.products),
    path('dashboard/orders', views.orders)
]