import os
import string
import random
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter
from .models import Product, Category, Cart, Order, Placed_Order, CustomUser
from .forms import UserForm, ProductForm, CategoryForm
from .serealisers import ProductSerializer
from .tokens import account_activation_token



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price']
    pagination_class = PageNumberPagination
    # filterset_fields = ['category']

    # own custom filter
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     hell = self.request.query_params.get('category_id')
    #     if hell is not None:
    #         queryset = queryset.filter(category=hell)
    #     return queryset

class Prod(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# class Prod(APIView):
#     def get(self,request,id):
#         obj = get_object_or_404(Product, id=id)
#         serializer = ProductSerializer(obj)
#         return Response(serializer.data)
#
#     def put(self,request,id):
#         obj = get_object_or_404(Product, id=id)
#         serializer = ProductSerializer(obj, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def delete(self, request, id):
#         obj = get_object_or_404(Product, id=id)
#         obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ProductAll(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# class ProductAll(APIView):
#     def get(self, request):
#         obj = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(obj, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


def email(request):
    return render(request, 'abpractice/email.html')
    # order = Order.objects.get(id=24)
    # products = Placed_Order.objects.filter(Q(order_id=24))
    # return render(request,'abpractice/email_template.html',{
    #    'order':order, 'products':products , 'user': request.user
    # })


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
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)
    form = AuthenticationForm()
    # return JsonResponse({'some_key': 'some_value'})
    return render(request, 'abpractice/login.html', {'form': form})


class FormCheck(View):

    def get(self, request, hell):
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
        check_stock = Product.objects.get(id=request.POST['product_id'])
        if check_stock.in_stock:
            queryset = Cart.objects.filter(
                Q(product_id=request.POST['product_id']) & Q(user_id=request.POST['user_id'])).first()
            if queryset:
                message = request.POST['title'] + ' Already added'
                return JsonResponse({'res': message})
            else:
                queryset = Cart(product_id=request.POST['product_id'], user_id=request.POST['user_id'],
                                quantity=request.POST['quantity'])
                queryset.save()
            # data = serializers.serialize('json', queryset)
            message = request.POST['title'] + ' Added to cart'
            html = render_to_string('abpractice/index.html', {'request': request})
            return JsonResponse({'res': message, 'html': html})
        else:
            message = 'Error'
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
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # all_entries = Category.objects.all().values()
            # mydict = {}
            # for entry in all_entries:
            #     mydict[entry['id']] = entry['category_name']
            form = ProductForm
            html = render_to_string('abpractice/add_product.html', {'pro_form': form, 'request': request})
            return JsonResponse({'html': html})
        form = ProductForm
        cat_form = CategoryForm
        return render(request, 'abpractice/add_product.html', {'pro_form': form, 'cat_form': cat_form})
    if request.method == 'GET':
        form = ProductForm
        cat_form = CategoryForm
        return render(request, 'abpractice/add_product.html', {'pro_form': form, 'cat_form': cat_form})


@user_passes_test(restricted_check)
@login_required(login_url='login')
def edit_product(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProductForm
            product = Product.objects.all()
            category = Category.objects.all()
            html = render_to_string('abpractice/edit_product.html',
                                    {'product': product, 'category': category, 'request': request})
            return JsonResponse({'html': html})
    product = Product.objects.all()
    category = Category.objects.all()
    cat_form = CategoryForm
    return render(request, 'abpractice/edit_product.html', {'product': product, 'category': category,
                                                            'cat_form': cat_form})


def delete(request, id):
    obj = get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('edit_product')
    return redirect('edit_product')


def update(request, id):
    if request.method == "POST":
        obj = Product.objects.get(id=id)
        try:
            if request.FILES['photo'] != 'Null':
                os.remove(obj.photo.path)

        except:
            pass
        try:
            if request.FILES['specs'] != 'Null':
                os.remove(obj.specs.path)
                obj.specs = request.FILES['specs']
        except:
            pass
        obj.title = request.POST['title']
        obj.description = request.POST['description']
        obj.price = request.POST['price']
        obj.in_stock = request.POST['in_stock']
        obj.category_id = request.POST['category']
        obj.save()
        return redirect('edit_product')
    return redirect('edit_product')


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
        html = render_to_string('abpractice/cart.html', {'carts': cart, 'request': request})
        return JsonResponse({'html': html, 'total': a})
    cart = Cart.objects.filter(Q(user_id=request.user.id))
    a = 0;
    for cat in cart:
        a += cat.product.price
    return render(request, 'abpractice/cart.html', {'carts': cart, 'total': a})


def order(request):
    if request.method == 'POST':
        carts = Cart.objects.filter(user_id=request.user.id)
        a = 0
        for cart in carts:
            if cart.product.in_stock:
                a += cart.product.price
                pass
            else:
                cart.delete()
                return redirect('cart')
        ref_code = unique_id()
        obj = Order(order_id=ref_code, total_price=a, user_id=request.user.id,
                    shipping_address=request.POST['shipping_address'])
        obj.save()
        for cart in carts:
            product_obj = Product.objects.get(id=cart.product.id)
            product_obj.in_stock -= 1
            product_obj.save()
            Placed_obj = Placed_Order(product_title=cart.product.title, product_photo=cart.product.photo,
                                      product_description=cart.product.description,
                                      product_price=cart.product.price,
                                      product_category=cart.product.category.category_name,
                                      order_id=obj.id, product_specs=cart.product.specs)
            Placed_obj.save()
            cart.delete()

        order = Order.objects.get(id=obj.id)
        products = Placed_Order.objects.filter(Q(order_id=obj.id))
        html_message = render_to_string(
            'abpractice/email_template.html', {'order': order, 'products': products, 'user': request.user})
        print(html_message)
        send_mail(
            'order',
            'saad bhai kya order krna a????',
            'test22123590@gmail.com',
            [request.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        orders = Order.objects.filter(user_id=request.user.id)
        return render(request, 'abpractice/order.html', {'orders': orders})

    if is_ajax(request) and request.method == "GET":
        products = Placed_Order.objects.filter(order_id=request.GET['order_id'])
        html = render_to_string('abpractice/order.html', {'products': products, 'request': request})
        return JsonResponse({'html': html})

    orders = Order.objects.filter(user_id=request.user.id)
    return render(request, 'abpractice/order.html', {'orders': orders})


def unique_id():
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=16))
    orders = Order.objects.filter(order_id=res)
    if orders:
        unique_id()
    return res


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('abpractice/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message, from_email='test22123590@gmail.com')

            messages.success(request, 'Please Confirm your email to complete registration.')
            return redirect('email')
            ######################### mail system ####################################
            # htmly = get_template('abpractice/email.html')
            # d = { 'username': username }
            # subject, from_email, to = 'welcome', 'test22123590@gmail.com', email
            # html_content = htmly.render(d)
            # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            # ##################################################################
            # messages.success(request, f'Your account has been created ! You are now able to log in')
            # return redirect('login')
    else:
        form = UserForm()
    return render(request, 'abpractice/register.html', {'form': form, 'title': 'register here'})


# def ajax_del(request):
# if request.method == "GET":
#     print(request.GET)
#     obj = get_object_or_404(Cart, id=request.POST['cart_id'])
#     print(obj)
# obj.delete()


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            # user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('verified')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been'
                                       ' used.'))
            return redirect('login')


def verified(request):
    return render(request, 'abpractice/verified_account.html')
