"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from login.views import signup_view
from products.views import (
    add_product_view,
    edit_product_view,
    edit_product_detail_view,
    home_view,
    delete_product_view,
    add_item_inventory_view,
    edit_item_inventory_view,
    delete_item_inventory_view,
    delete_image_view,
    product_detail_view,
    add_cart_item_view,
    cart_view,
    remove_from_cart_view,
)
from user.views import (
    account_view
)

urlpatterns = [
    path('account/', account_view, name='account'),
    path('remove_item_cart/<int:cart_item_id>', remove_from_cart_view, name='remove_item_cart'),
    path('cart/', cart_view, name='cart'),
    path('product/add_to_cart/', add_cart_item_view, name='add_cart_item'),
    path('product/<int:product_id_model>', product_detail_view, name='product_detail'),  # noqa: E501
    path('administration/inventory/image/delete/<int:product_id>/<int:image_id>/<str:gender>', delete_image_view, name='delete_image'),  # noqa: E501
    path('administration/inventory/delete/<int:product_id>/<int:item_id>', delete_item_inventory_view, name='delete_item_inventory'),  # noqa: E501
    path('administration/inventory/edit/<int:item_id>', edit_item_inventory_view, name='edit_item_inventory'),  # noqa: E501
    path('administration/inventory/<int:product_id>', add_item_inventory_view, name='add_item_inventory'),  # noqa: E501
    path('administration/edit/products/<int:product_id>/', edit_product_detail_view, name='edit_product_detail'),  # noqa: E501
    path('administration/edit/products/<int:force_delete_flag>/<int:product_id>/', edit_product_view, name='edit_product_force_delete'),  # noqa: E501
    path('administration/edit/products/', edit_product_view, name='edit_product'),  # noqa: E501
    path('administration/add_product/', add_product_view, name='add_product'),
    path('administration/', TemplateView.as_view(template_name='administration/administration.html'), name='administration'),  # noqa: E501
    path('account/signup/', signup_view),
    path('account/', include('django.contrib.auth.urls')),
    path('delete_product/<int:force_delete_flag>/<int:product_id>', delete_product_view, name='delete_product'),  # noqa: E501
    path('<str:gender>', home_view, name='home'),  # noqa: E501
    path('', home_view, name='home'),
    path("admin/", admin.site.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
