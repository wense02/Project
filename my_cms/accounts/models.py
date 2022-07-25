from django.db import models

# Create your models here.

class Customer (models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Template(models.Model):
    CATEGORY = (
        ('porfolio', 'porfolio'),
        ('ecommerce', 'ecommerce'),
        ('education', 'education'),
        ('health', 'health')
    )
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    views = models.CharField(max_length=200, null=True)
    pages = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class Website(models.Model):
    STATUS = (
        ('Incomplete', 'Incomplete'),
        ('Completed', 'Completed'),
        ('Hosted', 'Hosted')
    )
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)


    