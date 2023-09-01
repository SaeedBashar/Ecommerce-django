from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save()
            return redirect('/')
        
    else:
         form = UserCreationForm()
    return render(request, "registration/signup.html", {'form':form})