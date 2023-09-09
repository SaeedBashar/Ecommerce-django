from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
import json
from .forms import CustomRegistrationForm
from store.models import Customer

# Create your views here.

def SignUp(request):
    print(request.POST)
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            customer = Customer.objects.create()
            customer.name = user.first_name + " " + user.last_name
            customer.email = user.email
            customer.contact = request.POST.get('contact')
            customer.user = user

            customer.save()

            return redirect('/accounts/login')
        
        print(request.POST['email'])
        print(request.POST['first_name'])
        
    else:
        form = CustomRegistrationForm()
    return render(request, "registration/signup.html", {'form':form})
