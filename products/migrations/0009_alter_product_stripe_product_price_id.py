# Generated by Django 3.2.15 on 2023-09-16 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_stripe_product_price_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stripe_product_price_id',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
    ]