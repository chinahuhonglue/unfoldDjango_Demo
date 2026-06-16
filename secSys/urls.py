"""
URL configuration for secSys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect
from data.views import download_memorial_photo, memorial_photo_page
from secSys.admin_views import security_dashboard

urlpatterns = [
    path("", lambda request: redirect("admin:index"), name="home"),

    path("memorial/", memorial_photo_page, name="memorial_photo_page"),
    path("memorial/download/", download_memorial_photo, name="memorial_photo_download"),

    path("admin/security-dashboard/",admin.site.admin_view(security_dashboard), name="security_dashboard",),
    
    path("admin/", lambda request: redirect("security_dashboard"), name="admin_index_redirect"),

    path("admin/", admin.site.urls),
]
