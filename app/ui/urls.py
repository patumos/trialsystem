from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from . import views

urlpatterns = [
        path('', views.index, name='ui-index'),
        path('index2/', views.index2, name='ui-index2'),
        path('dashboard/', views.dashboard, name='ui-dashboard'),
        path('test/', views.test),
        path('trailrevise', views.trialRevise, name = "trial-revise"),
        path('updateform', views.updateform, name = "updateform")
        ]

