from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import WebsiteForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )
            messages.success(request, 'Account created successfully')
            return redirect('login')
    context = {'form' :form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
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
    return render (request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    websites = Website.objects.all()
    customers = Customer.objects.all()
    total_websites = websites.filter(status='Hosted').count()
    incomplete_websites = websites.filter(status='Incomplete').count()
    context = {'websites': websites, 'customers': customers, 'total_websites': total_websites, 'incomplete_websites': incomplete_websites}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def CustomerPage(request):
    websites = request.user.customer.website_set.all()
    total_websites = websites.count()
    incomplete_websites = websites.filter(status='Incomplete').count()
    context = {'websites': websites, 'total_websites':total_websites, 'incomplete_websites': incomplete_websites}
    return render(request, 'accounts/customer_dashboard.html', context)


@login_required(login_url='login')
def templates(request):
    templates = Template.objects.all()
    return render(request, 'accounts/templates.html', {'templates': templates})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    websites = customer.website_set.all()
    website_count = websites.count()
    context = {'customer':customer, 'websites': websites, 'website_count': website_count}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
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
@allowed_users(allowed_roles=['Admin'])
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
@allowed_users(allowed_roles=['Admin'])
def deleteWebsite(request, pk):
    website = Website.objects.get(id=pk)
    if request.method == 'POST':
        website.delete()
        return redirect('/')
    context = {'item': website}
    return render(request, 'accounts/delete.html', context)