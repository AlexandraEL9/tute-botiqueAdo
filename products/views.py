from django.shortcuts import render
from .models import Product

# Create your views here.

def all_products(request):
    """ A view to show all products, inc sorting and search """

    products = Product.objects.all()

    context = {
        'products': products,  # Corrected typo here
    }

    return render(request, 'products/products.html', context)
