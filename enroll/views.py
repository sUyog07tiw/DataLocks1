from django.shortcuts import render, redirect
from .models import Job, Application
from .forms import JobForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.files.storage import FileSystemStorage

@login_required(login_url='login')  # Ensure the user is logged in
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

@login_required(login_url='login')  # Ensure the user is logged in
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def post_job(request, job_id=None):
    if job_id:
        # Update an existing job post
        job = get_object_or_404(Job, id=job_id)
    else:
        job = None  # No job means creating a new one

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            if job:
                messages.success(request, 'Job updated successfully!')
            else:
                messages.success(request, 'Job posted successfully!')
            return redirect('job_list')
    else:
        form = JobForm(instance=job)

    return render(request, 'post_job.html', {'form': form, 'job': job})

@login_required(login_url='login')  # Ensure the user is logged in
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job created successfully!')
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'create_job.html', {'form': form})

@login_required(login_url='login')  # Ensure the user is logged in
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def applicant_list(request):
    return render(request, 'applicant_list.html')

@login_required(login_url='login')  # Ensure the user is logged in
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_detail(request, job_id):
    # Retrieve the job by its primary key (id)
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'job_detail.html', {'job': job})

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)  # Get the job object from the database

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        resume = request.FILES.get('resume')

        # Debugging: print out the data to make sure it's received
        print("Form Data:", request.POST)
        print("File Data:", request.FILES)

        # Check if the required fields are missing
        if not name or not email or not resume:
            messages.error(request, "All fields are required. Please fill in all fields and upload a resume.")
            return redirect('apply_job', job_id=job.id)

        # Check if the user has already applied for this job
        if Application.objects.filter(job=job, email=email).exists():
            messages.warning(request, "You have already applied for this job.")
            return redirect('job_detail', job_id=job.id)

        # Save the job application to the database
        try:
            application = Application.objects.create(
                job=job,
                name=name,
                email=email,
                resume=resume  # Resume is automatically stored by Django FileField
            )
            messages.success(request, "You have successfully applied for the job!")
            return redirect('job_detail', job_id=job.id)  # Redirect to job details page after applying
        except Exception as e:
            # Handle any errors that might occur while saving the application
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('apply_job', job_id=job.id)

    return render(request, 'apply.html', {'job': job})
    
@login_required(login_url='login')  # Ensure the user is logged in
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def base_view(request):
    return render(request, 'job_list.html') 

