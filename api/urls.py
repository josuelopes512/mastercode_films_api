"""mastercode_films_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('post', MovieView.as_view()),
    path('post_v2', moviePost),
    # path('get', MovieListView.as_view()),
    path('get', movieList),
    path('get_id/<str:pk>', movieList_id),
    # path('post', moviePost),
    path('put/<str:pk>', moviePut),
    path('delete/<str:pk>', movieDelete),
    # path('create', MovieCreateView.as_view()),
    # path('delete', MovieDeleteView.as_view()),
    # path('', MovieView.as_view()),
]
