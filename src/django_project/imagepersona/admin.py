from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Image)
admin.site.register(ImageSubFolder)
admin.site.register(ImageFolder)
admin.site.register(UserProfile)
admin.site.register(ImageTag)
admin.site.register(APIcalls)
