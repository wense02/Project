from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def home(request):
    websites = Website.objects.all()
    customers = Customer.objects.all()
    total_websites = websites.filter(status='Hosted').count()
    total_templates = Template.objects.all().count()
    context = {'websites': websites, 'customers': customers, 'total_websites': total_websites, 'total_templates': total_templates}
    return render(request, 'accounts/dashboard.html', context)

def templates(request):
    templates = Template.objects.all()
    return render(request, 'accounts/templates.html', {'templates': templates})

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    websites = customer.website_set.all()
    website_count = websites.count()
    context = {'customer':customer, 'websites': websites, 'website_count': website_count}
    return render(request, 'accounts/customer.html', context)