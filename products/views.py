from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'title': 'Store',

    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Store',
        'products': [
            {
                'name': 'Product 1',
                'price': 100
            },
            {
                'name': 'Product 2', 'price':200
            },

        ]
    }

    return render(request, 'products/products.html', context)
