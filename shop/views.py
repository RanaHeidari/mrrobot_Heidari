from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

def category_summary(request):
    all_cat = Category.objects.all()
    return render(request, 'category_summary.html', { 'category': all_cat })


def helloworld(request):
     all_products = Product.objects.all()

     return render(request,'index.html', { 'products':all_products })

def about(request):
     return render(request, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")
            return redirect("home")
        else:
            messages.success(request, "مشکلی در لاگین وجود داشت")
            return redirect("login")
    else:
        return render(request, 'login.html')
def logout_user(request):
    logout(request)
    messages.success(request,("با موفقیت خارج شدید"))
    return redirect("home")

def signup_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "این ایمیل قبلاً ثبت شده است.")
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                login(request, user)
                messages.success(request, "اکانت شما با موفقیت ساخته شد.")
                return redirect('home')
        else:
            messages.error(request, "رمزهای عبور مطابقت ندارند.")
    return render(request, 'signup.html')

def product(request, pk):
    product = Product.objects.get(id = pk)
    return render(request, 'product.html', {'product': product})

def category(request, cat):
    cat = cat.replace("-"," ")
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})

    except:
        messages.success(request, "دسته بندی مورد نظر وجود ندارد")
        return redirect("home")

