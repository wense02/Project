# Generated by Django 4.0.6 on 2022-07-25 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customer_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='firstname',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='lastname',
        ),
    ]
