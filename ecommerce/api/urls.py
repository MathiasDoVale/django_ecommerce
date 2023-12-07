from django.urls import path
from .views import (
    register_user,
    user_login,
    user_logout,
    home_products,
    product_detail
)

urlpatterns = [
    path('products/<int:product_id_model>', product_detail, name='product_detail'),
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home_products, name='home')
]
