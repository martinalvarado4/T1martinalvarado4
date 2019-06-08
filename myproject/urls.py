"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    #path('', include('swar.urls')),
    path('', views.index, name='index'),
    path('movies', views.index, name='index'),
    path('movies/<str:movie>', views.movie, name='movie'),
    path('characters/<str:character>', views.character, name='character'),
    path('planets/<str:planet>', views.planet, name='planet'),
    path('starships/<str:starship>', views.starship, name='starship'),
    path('result/', views.result, name='result'),
    path('admin/', admin.site.urls)
]
