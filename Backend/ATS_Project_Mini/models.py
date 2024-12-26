from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)




class User(models.Model):
    email = models.EmailField(unique=True, primary_key=True)  # Email is unique and serves as the primary key
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    dob = models.DateField()
    age = models.IntegerField()
    password = models.CharField(max_length=128)  # Store hashed password
    confirm_password = models.CharField(max_length=128)  # For validation (we will not store this)

    def __str__(self):
        return self.email