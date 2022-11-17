from django.urls import path
from . import views
urlpatterns = [
path('login/', views.login_user, name="login"),
path('index/', views.index, name="index"),
path('abpract/<slug:hell>', views.FormCheck.as_view()),
path('add_product/', views.add_product, name="add_product"),
path('edit_product/', views.edit_product, name="edit_product"),
path('logout/', views.logout_user, name="logout")
#     ,
# path('update/', views.update, name="update")
]