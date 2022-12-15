from django.conf.urls.static import static
from django.template.defaulttags import url
from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from django.conf import settings
from rest_framework.routers import SimpleRouter

from .views import ProductViewSet

router = SimpleRouter()
router.register('products',ProductViewSet,basename='products')

urlpatterns = [
path('', include(router.urls)),
path('login/', views.login_user, name="login"),
path('index/', views.index, name="index"),
# path('product/<int:pk>', views.Prod.as_view()),
# path('product', views.ProductAll.as_view()),
path('abpract/<slug:hell>', views.FormCheck.as_view()),
path('add_product/', views.add_product, name="add_product"),
path('edit_product/', views.edit_product, name="edit_product"),
path('logout/', views.logout_user, name="logout"),
path('update/<int:id>', views.update, name="update"),
path('delete/<int:id>', views.delete, name="delete"),
path('cart/', views.cart, name="cart"),
path('order/', views.order, name="order"),
path('register/', views.register, name ='register'),
path('email/', views.email, name ='email'),
path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
path('verified/', views.verified, name='verified'),
# path('cart/ajax/', views.ajax_del, name="ajax_del")
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
