import django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import CustomUser

import json

# Create your views here.
def log_in(request):
	template="custom_user/login.html"
	return render(request,template)

def verify_login(request):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect(reverse("custom_user:home"))
        else:
                #Redirect with failure
                template = "custom_user/login.html"
                data = {"Error" : "Email/Password is/are incorrect"}
                context = {'d' : data}
                return render(request, template, context = context)

def log_out(request):
	logout(request)
	return redirect(reverse("custom_user:login"))

def delete(request):
        request.user.delete()
        logout(request)
        return redirect(reverse("custom_user:home"))

def signup(request):
        template = "custom_user/signup.html"
        return render(request, template)

def verify_signup(request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        if not username or not email:
                template = "custom_user/signup.html"
                data = {"Error" : "Username and email id can't be empty"}
                context = {'d' : data}
                return render(request, template, context = context)

        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if password != cpassword:
                template = "custome_user/signup.html"
                data = {"Error": "Password and Confirm Passsword Do Not Match"}
                context = {'d':  data}
                return render(request, template, context = context)

        flatnumber = request.POST.get('flatnumber')
        vname = request.POST.get('vname')
        cityname = request.POST.get('cityname')
        pcode = request.POST.get('pcode')
        state = request.POST.get('state')

        address = f"Flat No. {flatnumber}, Village/Town {vname} City {cityname} State {state} Pin Code {pcode}"
        try:
                new_user = CustomUser.objects.create_user(email=email,
                                                          password=password,
                                                          username=username,
                                                          address = address,
                                                          )
                new_user.is_active = True
                new_user.save()
        except django.db.utils.IntegrityError:
                print ("Uplicate ID Error")
                template = "custom_user/signup.html"
                data = {"Error" : "Username/Email id already exists"}
                return render(request, template, data)

        return redirect(reverse('custom_user:login'))


@login_required(login_url='custom_user:login')
def home(request):
        template = "custom_user/home.html"
        user_data = CustomUser.objects.get(email=request.user.email)
        data = {"username" : user_data.username , "email" : user_data.email , "address" : user_data.address}
        context = {'d': data}
        return render(request,template,context)
