from django.urls import path

from products.views import *

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('product/<slug:product_id>/', ProductDetailView.as_view(), name='product'),
    path('category/<int:category_id>', ProductsListView.as_view(), name='category'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>', basket_remove, name='basket_remove'),
    path('search/', ProductsListView.as_view(), name='search'),
]
