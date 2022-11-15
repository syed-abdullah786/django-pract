from django.urls import path
from . import views
urlpatterns = [
path('', views.login),
path('abpract/<slug:hell>', views.FormCheck.as_view()),
path('detail/', views.details)
]