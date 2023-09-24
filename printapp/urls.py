from django.urls import path

from . import views

urlpatterns = [
    path('send_print', views.send_print),
]

