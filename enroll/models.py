from django.db import models

# Create your models here.
from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, choices=[('full-time', 'Full-time'), ('part-time', 'Part-time'), ('contract', 'Contract'), ('freelance', 'Freelance')])
    description = models.TextField()
    salary = models.CharField(max_length=50)
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} applied for {self.job.title}"