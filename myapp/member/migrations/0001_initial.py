# Generated by Django 5.1.3 on 2024-11-29 21:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('payment_method', models.CharField(choices=[('COD', 'Cash on Delivery'), ('CARD', 'Card Payment')], default='COD', max_length=10)),
                ('card_type', models.CharField(blank=True, choices=[('CIB', 'CIB'), ('QNB', 'QNB'), ('MEEZA', 'Meeza')], max_length=5)),
                ('payment_status', models.CharField(choices=[('SUCCEEDED', 'Succeeded'), ('FAILED', 'Failed'), ('PENDING', 'Pending')], default='PENDING', max_length=10)),
                ('total_amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.TextField()),
                ('price', models.FloatField()),
                ('product_category', models.CharField(choices=[('Accessories', 'Accessories'), ('Men Clothes', 'Men Clothes'), ('Women Clothes', 'Women Clothes'), ('Kids Clothes', 'Kids Clothes')], default='Accessories', max_length=50)),
                ('size', models.CharField(blank=True, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double Extra Large')], max_length=5, null=True)),
                ('accessory_type', models.CharField(blank=True, choices=[('Ring', 'Ring'), ('Handbag', 'Handbag'), ('Bracelet', 'Bracelet'), ('Necklace', 'Necklace')], max_length=50, null=True)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart_items', models.JSONField(default=list)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
