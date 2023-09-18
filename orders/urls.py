from django.urls import path
from django.views.decorators.cache import cache_page

from orders.views import *


app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
    path('', OrderListView.as_view(), name='orders_list'),

]
