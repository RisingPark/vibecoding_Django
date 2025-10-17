"""
URL configuration for memojjang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from apps.users import views as user_views
from apps.memos import views as memo_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", user_views.home, name="home"),
    path("register/", user_views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("memos/", memo_views.memo_list, name="memo_list"),
    path("memos/new/", memo_views.memo_create, name="memo_create"),
    path("memos/<int:pk>/", memo_views.memo_detail, name="memo_detail"),
    path("memos/<int:pk>/edit/", memo_views.memo_update, name="memo_update"),
    path("memos/<int:pk>/delete/", memo_views.memo_delete, name="memo_delete"),
]
