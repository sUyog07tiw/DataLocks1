from django.contrib import admin
from django.urls import path, include
from accounts import views  
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('', LogoutView.as_view(template_name='login.html'), name='index'),