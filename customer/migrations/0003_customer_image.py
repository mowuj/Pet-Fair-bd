# Generated by Django 4.2 on 2024-01-17 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_customer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='customer/images'),
        ),
    ]
