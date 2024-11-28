from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - спасибо за заказ'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - заказы'
    queryset = Order.objects.all()
    ordering = ('-id',)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - оформление заказа'

    def form_valid(self, form):
        # Set the initiator of the order (the user making the order)
        form.instance.initiator = self.request.user

        # Save the order to the database
        response = super(OrderCreateView, self).form_valid(form)

        # Retrieve the user's basket
        baskets = Basket.objects.filter(user=self.request.user)

        # Save the basket details to the order
        form.instance.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        form.instance.save()

        # Delete items from the basket after order creation
        baskets.delete()

        return response



@csrf_exempt
def stripe_webhook_view(request):
    return HttpResponse(status=200)
