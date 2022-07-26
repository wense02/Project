from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Website, Customer
from django.contrib.auth.models import User

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class WebsiteForm(ModelForm):
    class Meta:
        model = Website
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

