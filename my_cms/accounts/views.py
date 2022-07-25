from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import WebsiteForm

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

def createWebsite(request):
    form = WebsiteForm()
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/website_form.html', context)

def updateWebsite(request, pk):
    website = Website.objects.get(id=pk)
    form = WebsiteForm(instance=website)
    if request.method == 'POST':
        form = WebsiteForm(request.POST, instance=website)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/website_form.html', context)

def deleteWebsite(request, pk):
    website = Website.objects.get(id=pk)
    if request.method == 'POST':
        website.delete()
        return redirect('/')
    context = {'item': website}
    return render(request, 'accounts/delete.html', context)