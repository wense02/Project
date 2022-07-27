from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import WebsiteForm, CreateUserForm, CustomerForm
from .decorators import unauthenticated_user, allowed_users, admin_only

#new imports for reset password
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
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
@allowed_users(allowed_roles=['Customer'])
def accountSettings(request): 
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


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


#Password reset view
def password_reset_request(request):
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "accounts/password/password_reset_email.txt"
                        c = {
                            "email":user.email,
                            'domain':'127.0.0.1:8000',
					        'site_name': 'Website',
					        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
					        "user": user,
					        'token': default_token_generator.make_token(user),
					        'protocol': 'http',
                            }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                        except BadHeaderError:
                               return HttpResponse('Invalid header found.')
                        return redirect ("/password_reset/done/")
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="accounts/password/password_reset.html", context={"password_reset_form":password_reset_form})