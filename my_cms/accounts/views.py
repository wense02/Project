from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import WebsiteForm, CreateUserForm

# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created successfully')
                return redirect('login')

        context = {'form' :form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def home(request):
    websites = Website.objects.all()
    customers = Customer.objects.all()
    total_websites = websites.filter(status='Hosted').count()
    total_templates = Template.objects.all().count()
    context = {'websites': websites, 'customers': customers, 'total_websites': total_websites, 'total_templates': total_templates}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def templates(request):
    templates = Template.objects.all()
    return render(request, 'accounts/templates.html', {'templates': templates})

@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    websites = customer.website_set.all()
    website_count = websites.count()
    context = {'customer':customer, 'websites': websites, 'website_count': website_count}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def createWebsite(request):
    form = WebsiteForm()
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/website_form.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def deleteWebsite(request, pk):
    website = Website.objects.get(id=pk)
    if request.method == 'POST':
        website.delete()
        return redirect('/')
    context = {'item': website}
    return render(request, 'accounts/delete.html', context)