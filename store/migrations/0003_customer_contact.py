# Generated by Django 3.2.11 on 2023-09-09 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='contact',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
