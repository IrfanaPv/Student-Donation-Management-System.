from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class CoustomUser(AbstractUser):
    is_student=models.BooleanField(default=False)
    is_doner=models.BooleanField(default=False)
class Student(models.Model):
    user=models.OneToOneField('CoustomUser',on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    age=models.IntegerField()
    email=models.EmailField(max_length=40)
    contact_number=models.IntegerField()
    address=models.TextField()
class Donor(models.Model):
    user=models.OneToOneField('CoustomUser',on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=40)
    contact_number=models.IntegerField()
    address=models.TextField()
class Donation_request(models.Model):
    CATOGERY_CHOICES=[
          ('Books','Books'),
           ('Tution','Tution'),
           ('Uniform','Uniform'),
           ('Laptop','Laptop'),
           ('Others','Others'),
    ]
    stud=models.ForeignKey(Student,on_delete=models.CASCADE)
    catogery=models.CharField(max_length=20,choices=CATOGERY_CHOICES,default='Others')
    description=models.TextField()
    amount_needed=models.DecimalField(max_digits=10, decimal_places=2)
    location=models.CharField(max_length=100)
    id_document=models.FileField(upload_to='documents/id_docs/', null=True, blank=True)
    income_certificate=models.FileField(upload_to='documents/income_certs/', null=True, blank=True)
    status=models.CharField(max_length=20,choices=[('pending', 'Pending'),('approved', 'Approved'),('rejected', 'Rejected')], default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
class Donation(models.Model):
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)
    donation_request=models.ForeignKey(Donation_request,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    donated_at=models.DateTimeField(auto_now_add=True)

    