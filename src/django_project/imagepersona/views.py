from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.conf import settings
import httplib, urllib, base64, json
from django.http import JsonResponse

CF_headers = {
	# Request headers for CF API
	'Content-Type': 'application/json',
	'Ocp-Apim-Subscription-Key': settings.CF_KEY,
}

CF_detect_params = urllib.urlencode({
	# Request parameters
	'returnFaceId': 'true',
	'returnFaceLandmarks': 'false',
})

CF_group_params = urllib.urlencode({
})

def index(request):
	return HttpResponse("Main Index Page")

# user log in
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render(request, 'imagepersona/upload.html')
			else:
				return render(request, 'imagepersona/login.html', {'login_error_message': 'Your account has been disabled'})
		else:
			return render(request, 'imagepersona/login.html', {'login_error_message': 'Invalid login'})
	return render(request, 'imagepersona/login.html')

# User Log Out
def logout_user(request):
	logout(request)
	return render(request, 'imagepersona/login.html')

# Register New User
def register_user(request):
	if request.method == "POST":
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		user = User.objects.create_user(username, email, password)
		user.last_name = lastname
		user.first_name = firstname
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render(request, 'imagepersona/upload.html')
	return render(request, 'imagepersona/login.html')

@login_required(login_url='/imagepersona/login/')
def upload(request):
	if request.method=='POST':
		files = request.FILES.getlist("files")
		newAlbum = ImageFolder()
		newAlbum.name = request.POST["albumname"]
		newAlbum.save()
		request.user.userprofile.albums.add(newAlbum)
		FaceIDs = []
		for file in files:
			newImage = Image()
			newImage.image = file
			newImage.save()
			img_url = "http://" + request.get_host() + newImage.image.url
			body = json.dumps({ 'url': img_url })
			try:
				conn = httplib.HTTPSConnection(settings.CF_BASE_URL)
				conn.request("POST", "/face/v1.0/detect?%s" % CF_detect_params, body, CF_headers)
				response = conn.getresponse()
				data = response.read()
				res = json.loads(data)
				count = len(res)
				for x in range(0,count):
					resx = res[x]
					resx = resx["faceId"]
					resx = resx.encode('ascii')
					FaceIDs.append(resx)
				conn.close()
			except Exception as e:
				return HttpResponse(e)
				print(e)
				print("[Errno {0}] {1}".format(e.errno, e.strerror))

			newImage.json_response = data
			newImage.save()
		body = json.dumps({"faceIds" : FaceIDs })
		print(FaceIDs)
		try:
			conn = httplib.HTTPSConnection(settings.CF_BASE_URL)
			conn.request("POST", "/face/v1.0/group?%s" % CF_group_params, body, CF_headers)
			response = conn.getresponse()
			data = response.read()
			print(data)
			res = json.loads(data)
			print(res)
			# res = res["groups"]
			conn.close()
		except Exception as e:
			print(e)
			print("[Errno {0}] {1}".format(e.errno, e.strerror))
		return JsonResponse({'res':res})

	return render(request, 'imagepersona/upload.html')

@login_required(login_url='/imagepersona/login/')
def photos(request):
	albums = request.user.userprofile.albums.all()
	context = {}
	if albums is not None:
		context	['albums'] = albums
	return render(request, 'imagepersona/photos.html', context)


@login_required(login_url='/imagepersona/login/')
def profile(request):
	if request.method=='POST':
		updates = { 'profilepic' : 'not-updated',
						'coverpic' : 'not-updated'
						}
		if request.FILES.getlist("profile"):
			profile = request.FILES.getlist("profile")
			print request.user, profile[0]
			userpro = UserProfile.objects.filter(user=request.user)[0]
			userpro.profilepic = profile[0]
			print userpro.profilepic
			# userpro = request.user.userprofile()
			userpro.save()
			# newImage.image = profile
			# newImage.save()
			updates['profilepic'] = 'updated'
		if request.FILES.getlist("cover"):
			cover = request.FILES.getlist("cover")
			print request.user, cover[0]
			userpro = UserProfile.objects.filter(user=request.user)[0]
			userpro.coverpic = cover[0]
			print userpro.coverpic
			# userpro = request.user.usercover()
			userpro.save()
			# newImage.image = cover
			# newImage.save()
			updates['coverpic'] = 'updated'
		return render(request, 'imagepersona/profile.html', updates)
	return render(request, 'imagepersona/profile.html')

@login_required(login_url='/imagepersona/login/')
def album(request, album_id):
	album = get_object_or_404(ImageFolder, pk = album_id)
	myalbums = request.user.userprofile.albums.all()
	if(album in myalbums):
		return render(request, 'imagepersona/album.html', {'album_name':album.name, 'people':album.subfolders.all()})
	raise Http404("Album does not exist!")

@login_required(login_url='/imagepersona/login/')
def images(request):
	return render(request, 'imagepersona/images.html')
