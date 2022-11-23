from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from .models import Product, Category, Cart, Order, Placed_Order
from .forms import UserForm, ProductForm, CategoryForm, CartForm
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required, user_passes_test
def restricted_check(user):
    # return user.groups.filter(name='view_restrict_group').exists()
    if user.is_superuser:
        return True
    else:
        return False

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


@login_required(login_url='login')
def index(request):
    product = Product.objects.all()
    category = Category.objects.all()
    if request.method == 'POST' and is_ajax(request):
        queryset = Cart.objects.filter(
            Q(product_id=request.POST['product_id']) & Q(user_id=request.POST['user_id'])).first()
        print(request.POST['title'])
        if queryset:
            message = request.POST['title'] + ' Already added'
            return JsonResponse({'res': message})
        else:
            queryset = Cart(product_id=request.POST['product_id'], user_id=request.POST['user_id'], quantity=request.POST['quantity'])
            queryset.save()
        # data = serializers.serialize('json', queryset)
        message = request.POST['title'] + ' Added to cart'
        return JsonResponse({'res': message})
    return render(request, 'abpractice/index.html', {'product': product, 'category': category})



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
@user_passes_test(restricted_check)
@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = ProductForm
        cat_form = CategoryForm
        return render(request, 'abpractice/add_product.html', {'pro_form': form,'cat_form':cat_form})


@user_passes_test(restricted_check)
@login_required(login_url='login')
def edit_product(request):
    product = Product.objects.all()
    category = Category.objects.all()
    return render(request, 'abpractice/edit_product.html', {'product': product, 'category': category})


def delete(request, id):
    obj = get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('index')
    return redirect('index')


def update(request, id):
    if request.method == "POST":
        obj = Product.objects.get(id=id)
        obj.title = request.POST['title']
        obj.description = request.POST['description']
        obj.price = request.POST['price']
        obj.in_stock = request.POST['in_stock']
        obj.category_id = request.POST['category']
        obj.save()
        return redirect('index')
    return redirect('index')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def cart(request):
    if is_ajax(request) and request.method == "GET":
        obj = get_object_or_404(Cart, id=request.GET['cart_id'])
        obj.delete()
        cart = Cart.objects.filter(Q(user_id=request.user.id))
        a = 0;
        for cat in cart:
            a += cat.product.price
        html = render_to_string('abpractice/cart.html', {'carts': cart})
        return JsonResponse({'html': html, 'total': a})
    cart = Cart.objects.filter(Q(user_id=request.user.id))
    a = 0;
    for cat in cart:
        a += cat.product.price
    return render(request, 'abpractice/cart.html',{'carts': cart,'total':a})


def order(request):
    if request.method == 'POST':
        carts = Cart.objects.filter(user_id=request.user.id)
        a = 0;
        for cart in carts:
            if cart.product.in_stock:
                a += cart.product.price
                pass
            else:
                return redirect('cart')
        obj = Order(total_price=a, user_id=request.user.id,
                        shipping_address=request.POST['shipping_address'])
        obj.save()
        for cart in carts:
            product_obj = Product.objects.get(id=cart.product.id)
            product_obj.in_stock -= 1
            product_obj.save()
            Placed_obj = Placed_Order(product_title=cart.product.title, product_description=cart.product.description,
                               product_price=cart.product.price, product_category=cart.product.category.category_name,
                               order_id=obj.id)
            Placed_obj.save()
            cart.delete()
        orders = Order.objects.filter(user_id=request.user.id)
        return render(request, 'abpractice/order.html', {'orders': orders})
    orders = Order.objects.filter(user_id=request.user.id)
    return render(request, 'abpractice/order.html', {'orders': orders})


# def ajax_del(request):
    # if request.method == "GET":
    #     print(request.GET)
    #     obj = get_object_or_404(Cart, id=request.POST['cart_id'])
    #     print(obj)
        # obj.delete()
