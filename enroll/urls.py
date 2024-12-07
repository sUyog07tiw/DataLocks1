from django.urls import path
from . import views
from accounts.views import login_view 
from accounts.views import logout_view 

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job_list/', views.job_list, name='job_list'), 
    path('base/', views.base_view, name='base'),  # List all jobs
    path('job/create/', views.create_job, name='create_job'),  # Create a new job posting
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),  # Job detail view
    path('job/apply/<int:job_id>/', views.apply_job, name='apply_job'),  # Apply for a job
    path('applicants/', views.applicant_list, name='applicant_list'),  # List all applicants  # Logout functionality
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('login/', login_view, name='login'),
    path('jobs/post/', views.post_job, name='post_job'),]
