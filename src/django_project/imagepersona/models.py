from django.db import models
from django.contrib.auth.models import User

# User
class UserProfile(models.Model):
    user = models.OneToOneField(User)

# Main Albums uploaded by the user
class ImageFolder(models.Model):
	name = models.CharField(max_length=20)
	owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

# In the Main Albums, Divided in sub-folders according to the persons
class ImageSubFolder(models.Model):
	name = models.CharField(max_length=20)
	directory = models.ForeignKey(ImageFolder, on_delete=models.CASCADE)

# Images
class Image(models.Model):
	album = models.ForeignKey(ImageFolder, on_delete=models.CASCADE)
	image = models.ImageField(max_length=50)
	people = models.ManyToManyField(ImageSubFolder)
