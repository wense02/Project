# Generated by Django 4.0.6 on 2022-07-25 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_website_customer_website_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='website',
            old_name='product',
            new_name='template',
        ),
    ]