from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Images
class Image(models.Model):
	# album = models.ForeignKey(ImageFolder, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="images/")
	# owner = models.ForeignKey(UserProfile)
	# people = models.ManyToManyField(ImageSubFolder)
	def __str__(self):
		return self.image.name


# In the Main Albums, Divided in sub-folders according to the persons
class ImageSubFolder(models.Model):
	name = models.CharField(max_length=20)
	# directory = models.ForeignKey(ImageFolder, on_delete=models.CASCADE)
	images = models.ManyToManyField(Image)

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()