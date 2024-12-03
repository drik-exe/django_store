from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.db.models import Q

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductDetailView(DetailView):
    template_name = 'products/product.html'
    model = Product
    context_object_name = 'product_obj'
    pk_url_kwarg = 'product_id'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - catalog'
    ordering = ['quantity']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        queryset = queryset.filter(category_id=category_id) if category_id else queryset

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price or max_price:
            price_filter = Q()
            if min_price:
                price_filter &= Q(price__gte=min_price)
            if max_price:
                price_filter &= Q(price__lte=max_price)
            queryset = queryset.filter(price_filter)

        # New: Filter by quantity
        min_quantity = self.request.GET.get('min_quantity')
        max_quantity = self.request.GET.get('max_quantity')
        if min_quantity or max_quantity:
            quantity_filter = Q()
            if min_quantity:
                quantity_filter &= Q(quantity__gte=min_quantity)
            if max_quantity:
                quantity_filter &= Q(quantity__lte=max_quantity)
            queryset = queryset.filter(quantity_filter)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['q'] = self.request.GET.get('q')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        # Add min and max quantity to context
        context['min_quantity'] = self.request.GET.get('min_quantity', '')
        context['max_quantity'] = self.request.GET.get('max_quantity', '')
        return context





@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])



@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
