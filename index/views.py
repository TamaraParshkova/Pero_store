from django.shortcuts import render
from cart.forms import CartAddProductForm
from catalog.models import Category, Product

def homepage(request):
    cart_product_form = CartAddProductForm()
    categories = Category.objects.all()
    sale = Product.objects.exclude(discount = 0)
    hit = Product.objects.filter(hit = True)
    return render(request, 'index/homepage.html', locals())

def show_cat(request, cat_slug):
    cart_product_form = CartAddProductForm()
    cat = Category.objects.get(slug=cat_slug)
    prod= Product.objects.filter(category_id = cat.id)
    return render(request, 'index/cat.html', locals())

def about(request):
    return render(request, 'index/about.html', locals())

def product_search(request):
    query = (request.GET.get('query'))
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'index/search_results.html', locals())