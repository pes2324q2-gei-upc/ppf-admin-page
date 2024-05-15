"""
URL configuration for adminApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import include, path
from adminPage import views


urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('users/<int:pk>/', views.userDetails, name='userDetails'),
    path('reported/', views.reported, name='reports'),
    path('users/<int:pk>/reports/', views.userReportsDetails,
         name='userReportsDetails'),
    path('reports/<int:pk>/', views.reportDetails, name='reportsDetails'),
    path('users/<int:pk>/edit/', views.userDetailsEdit, name='userDetailsEdit'),
]