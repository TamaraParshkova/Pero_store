"""
URL configuration for stationery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from catalog import views as catalog
from index import views as index
from orders import views as orders
from users import views as users
from cart import views as cart



urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', cart.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', cart.cart_add, name='cart_add'),
    path('cart/decrease_item_quantity/<int:product_id>', cart.cart_decrease, name='decrease'),
    path('cart/remove/<int:product_id>', cart.cart_remove, name='cart_remove'),
    path('catalog/<slug:prod_slug>', catalog.show_prod, name='prod'),
    path('catalog/<slug:cat_slug>', index.show_cat, name='category'),
    path('catalog/', catalog.products, name ='products'),
    path('', index.homepage, name ='home'),
    path('about', index.about, name ='about'),
    path('search_results', index.product_search, name ='search_results'),
    path('users/login', users.LoginUser.as_view(), name='login'),
    path('users/registration/',  users.RegisterUser.as_view(), name='registration'),
    path('users/register_done/', TemplateView.as_view(template_name="users/register_done.html"), name='register_done'),
    path('users/profile/', users.ProfileUser.as_view(), name='profile'),
    path('users/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('orders/create_orders', orders.create_order, name='order'),
    
]
