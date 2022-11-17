from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from .forms import UserForm, ProductForm, CategoryForm
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
import json


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('index')

    else:
        form = AuthenticationForm()
    return render(request, 'abpractice/login.html', {'form': form})


class FormCheck(View):

    def get(self, request,hell):
        form = UserForm
        meetings = [
            {'title': 'with Qasim', 'location': 'at Gujrat'},
            {'title': 'with Ahsan', 'location': 'at Lahore'}
        ]
        return render(request, 'abpractice/index.html',
                      {'form': form,
                       'meets': meetings,
                       'show_meets': True})

    def post(self, request, hell):
        form = UserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return render(request, 'abpractice/detail.html')


def index(request):
    return render(request, 'abpractice/index.html')



# def index(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return render(request, 'abpractice/detail.html')
#     else:
#         form = UserForm
#
#     met = MeetUps.objects.all()
#     meetings = [
#             {'title': 'with Qasim', 'location': 'at Gujrat'},
#             {'title': 'with Ahsan', 'location': 'at Lahore'}
#         ]
#     return render(request, 'abpractice/index.html',
#                  {'form':form,
#                   'meets': meetings,
#                   'show_meets': True})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('index')
        form = CategoryForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('add_product')
    else:
        form = ProductForm
        cat_form = CategoryForm
        return render(request, 'abpractice/add_product.html', {'pro_form': form,'cat_form':cat_form})

def edit_product(request):
    product = Product.objects.all()
    print(product[0].category)
    # print(product['title'])
    return render(request, 'abpractice/edit_product.html',{'product': product})

# def update(request, id):