from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='root'),
    path('login/', views.login_view, name='login'), 
    path('signup/', views.signup_view, name='signup'),  
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('browse-jobs/', views.browse_jobs, name='browse_jobs'),
    path('delete-user/<int:user_id>/', views.delete_user_view, name='delete_user'),
]