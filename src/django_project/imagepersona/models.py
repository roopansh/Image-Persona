from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Images
class Image(models.Model):
	# album = models.ForeignKey(ImageFolder, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="images/")
	json_response = models.CharField(blank=True, max_length=1000)
	owner = models.ForeignKey(User)
	# people = models.ManyToManyField(ImageSubFolder)

	def __str__(self):
		return self.image.name


# In the Main Albums, Divided in sub-folders according to the persons
class ImageSubFolder(models.Model):
	name = models.CharField(max_length=20)
	# directory = models.ForeignKey(ImageFolder, on_delete=models.CASCADE)
	images = models.ManyToManyField(Image)
	#displayPic = models.ImageField(upload_to="displaypic/")
	displaypic = models.IntegerField(null=True, blank=True)
	personid = models.CharField(max_length = 50, null=True, blank=True)
	croppedDP = models.ImageField(null=True, blank=True, upload_to="images/")

	def __str__(self):
		return self.name


# Main Albums uploaded by the user
class ImageFolder(models.Model):
	name = models.CharField(max_length=20)
	# owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	subfolders = models.ManyToManyField(ImageSubFolder)

	def __str__(self):
		return self.name


# User
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	albums = models.ManyToManyField(ImageFolder, blank=True)
	profilepic = models.ImageField(verbose_name="Profile Pic", upload_to="users/", default="profilepic.jpg")
	coverpic = models.ImageField(verbose_name="Cover Pic", upload_to="users/", default="coverpic.jpg")

	def __str__(self):
		return self.user.get_full_name()


#Tags
class ImageTag(models.Model):
	name = models.CharField(max_length = 20, blank = False)
	images = models.ManyToManyField(Image)

	def __str__(self):
		return self.name

# Sharing Subfolders via Link
class linksharing(models.Model):
	reference = models.CharField(max_length = 50, blank = False)
	real = models.CharField(max_length = 80, blank = False)

	def __str__(self):
		return self.reference

# Verify email
class verifyEmail(models.Model):
	reference = models.CharField(max_length = 50, blank = False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.reference

# Forgot Password
class forgotPassword(models.Model):
	reference = models.CharField(max_length = 50, blank = False) # Unique ID
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.get_full_name()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.userprofile.save()
