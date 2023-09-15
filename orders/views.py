import stripe

from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.views.generic.base import TemplateView

from common.views import TitleMixin
from orders.forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - спасибо за заказ'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'

class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NqhsHEPWGH48RhK0nR7STo9',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=303)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)