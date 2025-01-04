

from django.contrib import admin
from django.urls import include, path
from .views import index
from .views import Node
urlpatterns = [
    
    path('createNode/',Node.as_view(),name="createNode"),
    path('getNode/',Node.as_view(),name="getNode"),
    path('', index),
]
