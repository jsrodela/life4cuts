from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('startpage', views.startpage),
    path('background', views.background),
    path('guide', views.guide),
    path('cam', views.cam),
    path('picturechoose', views.picturechoose),
    path('framechoose', views.framechoose),
    path('wstest', views.wstest),
    path('loading', views.loading),
    path('end', views.end),
    path('test/<str:name>', views.test)
]

