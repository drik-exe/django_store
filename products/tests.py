from django.test import TestCase
from django.urls import reverse

from products.models import Product
from users.models import User


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        products = Product.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(list(response.context_data['object_list']), list(products[:3]))
