from django.http import HttpResponse, Http404, JsonResponse, HttpResponseNotFound#, HttpResponceRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from .models import *
from django.conf import settings
import httplib, urllib, base64, json
from datetime import datetime
import time
from django.core.mail import send_mail
from collections import Counter
from PIL import Image as PILImage
import zipfile, StringIO
import os
from django.core.files import File
from django.core.files.base import ContentFile
import threading
from django.utils.timezone import utc
from django.contrib import messages
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

CV_headers = {
	# Request headers for CF API
	'Content-Type': 'application/json',
	'Ocp-Apim-Subscription-Key': settings.CV_KEY,
}

CV_params = urllib.urlencode({
	# Request parameters. All of them are optional.
	'visualFeatures': 'Tags',
	'language': 'en',
})

unclassifiedFile = open(settings.MEDIA_ROOT + "/unclassified.png", 'rb')
unclassified_DP_django_file = File(unclassifiedFile)


def index(request):
	return render(request, 'imagepersona/index.html')

# user log in
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('imagepersona:upload')
				return render(request, 'imagepersona/upload.html')
			else:
				return render(request, 'imagepersona/login.html', {'login_error_message': 'Pending email verfication'})
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
		if User.objects.filter(username=username):
			return render(request, 'imagepersona/login.html', {'login_error_message' : "Username already taken.",'register_error_message' : "Username already taken."})
		if User.objects.filter(email=email):
			return render(request, 'imagepersona/login.html', {'register_error_message' : "Email already registered.", 'login_error_message' : "Email already registered."})
		user = User.objects.create_user(username, email, password)
		user.last_name = lastname
		user.first_name = firstname
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				unique_id = get_random_string(length=20)
				ver = verifyEmail()
				ver.reference = unique_id
				ver.user = user
				ver.save()
				link_url = "http://" + request.get_host() + '/imagepersona/verify/' + unique_id
				# TODO: Convert this to HTML
				send_mail(
					'Verify your Account',
					'Dear ' + user.get_full_name() + ',\n\nClick on this link to verify your email.\n\n' + link_url + '\n\nIf you didn\'t register, please ignore.\n\n--\n\nTeam Image Persona',
					'contact.imagepersona@gmail.com',
					[user.email],
					fail_silently=False,
				)
				user.is_active = False
				user.save()
				return render(request, 'imagepersona/login.html', {'login_error_message': 'An email has been sent. Verify your email.'})
	return render(request, 'imagepersona/login.html')

@login_required(login_url='/imagepersona/login/')
def upload(request):
	if request.method=='POST':
		newAlbum = ImageFolder()
		newAlbum.name = request.POST["albumname"]
		newAlbum.save()
		request.user.userprofile.albums.add(newAlbum)
		savedImages = []
		for file in request.FILES.getlist("files"):
			print(str(file).split('.')[-1])
			if str(file).split('.')[-1] in ['jpg','jpeg','png','gif', 'bmp']:
				newImage = Image()
				newImage.image = file
				newImage.owner = request.user
				newImage.save()
				savedImages.append(newImage)

		# Start a thread to Group Images
		t = threading.Thread(target=ClassifyImages, args=(savedImages, newAlbum, request.user, request.get_host()))
		t.daemon = True
		t.start()
		messages.success(request, 'Photos Uploaded Successfully. Photos are being grouped. An email will be sent to you when the Grouping finishes!')
		return redirect('imagepersona:album', album_id=newAlbum.pk)
	return render(request, 'imagepersona/upload.html')

@login_required(login_url='/imagepersona/login/')
def photos(request):
	albums = request.user.userprofile.albums.all()
	context = {}
	if albums is not None:
		context	['albums'] = albums
	return render(request, 'imagepersona/photos.html', context)

@login_required(login_url='/imagepersona/login/')
def searchPhotos(request):
	queryTerms = request.GET["query"].split()
	result = Counter() # USE counter
	for keyword in queryTerms:
		# Tag Search
		tags = ImageTag.objects.filter(name__icontains = keyword)
		for tag in tags:
			for image in tag.images.all():
				if image.owner is request.user:
					result[image] += 2
		# Person Search
		persons = ImageSubFolder.objects.filter(name__icontains = keyword)
		for person in persons:
			for image in person.images.all():
				if image.owner == request.user:
					result[image] += 3
		# Album Search
		albums = ImageFolder.objects.filter(name__icontains = keyword)
		for album in albums:
			for person in album.subfolders.all():
				for image in person.images.all():
					if image.owner == request.user:
						result[image] += 1
	res = result.most_common()
	try:
		topScore = res[0][1]
	except Exception:
		topScore = 0
	result = []
	for item in res:
		if item[1] <= settings.SEARCH_FACTOR * topScore :
			break
		result.append(item[0])
	context = {
		"query" : request.GET["query"],
		"result" : result,
	}
	return render(request, 'imagepersona/search.html', context)


@login_required(login_url='/imagepersona/login/')
def profile(request):
	if request.method=='POST':
		updates = { 'profilepic' : 'not-updated',
					'coverpic' : 'not-updated',
					'firstname' : 'not-updated',
					'lastname' : 'not-updated',
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
			messages.success(request, 'Profile Picture Updated!')
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
			messages.success(request, 'Cover Picture Updated!')
			updates['coverpic'] = 'updated'
		if request.POST["firstname"]:
			firstname = request.POST["firstname"].strip().encode("ascii")
			if firstname != "":
				request.user.first_name = firstname
				messages.success(request, 'First Name Updated!')
				updates['firstname'] = 'updated'
		if request.POST["lastname"]:
			lastname = request.POST["lastname"].strip().encode("ascii")
			if lastname != "":
				request.user.last_name = lastname
				messages.success(request, 'Last Name Updated!')
				updates['lastname'] = 'updated'
		request.user.save()
		return redirect('imagepersona:profile')
	return render(request, 'imagepersona/profile.html')

@login_required(login_url='/imagepersona/login/')
def album(request, album_id):
	album = get_object_or_404(ImageFolder, pk = album_id)
	myalbums = request.user.userprofile.albums.all()
	if(album in myalbums):
		print(album)
		for person in album.subfolders.all():
			if not person.croppedDP :
				displaypic = Image.objects.get(pk = person.displaypic)
				displayid = person.personid
				json_response = json.loads(displaypic.json_response)
				for item in json_response:
					if item["faceId"] == displayid:
						top = item["faceRectangle"]["top"]
						left = item["faceRectangle"]["left"]
						right = item["faceRectangle"]["left"] + item["faceRectangle"]["width"]
						bottom = item["faceRectangle"]["top"] + item["faceRectangle"]["height"]
						person.croppedDP.save(displaypic.image.url.split('/')[-1],displaypic.image.file,save=True)
						person.save()
						temp = PILImage.open(person.croppedDP.path)
						tempImg = temp.crop((left, top, right, bottom))
						tempImg.save(person.croppedDP.path)
						break
		return render(request, 'imagepersona/album.html', {'album_name':album.name, 'people':album.subfolders.all(), 'albumPk' : album.pk})
	raise Http404("Album does not exist!")

@login_required(login_url='/imagepersona/login/')
def images(request, album_id, person_id):
	album = get_object_or_404(ImageFolder, pk = album_id)
	myalbums = request.user.userprofile.albums.all()
	if(album in myalbums):
		peopleInthisFolder = album.subfolders.all()
		person = get_object_or_404(ImageSubFolder, pk = person_id)
		context = {'images' : person.images.all(), 'PersonName' : person.name, 'album' : album, 'personId' : person.pk, 'displaypic':person.croppedDP.url}
		return render(request, 'imagepersona/images.html', context)
	raise Http404("Person group does not exist!")

@login_required(login_url='/imagepersona/login/')
def editSubfolder(request, album_id, person_id):
	if request.method=='POST':
		album = get_object_or_404(ImageFolder, pk = album_id)
		myalbums = request.user.userprofile.albums.all()
		if(album in myalbums):
			peopleInthisFolder = album.subfolders.all()
			person = get_object_or_404(ImageSubFolder, pk = person_id)
			if(person in peopleInthisFolder):
				person.name = request.POST['Personname']
				person.save()
				messages.success(request, 'Name updated to ' + str(person.name))
				return redirect('imagepersona:images', album_id=album_id, person_id=person_id)
	raise Http404("Person group does not exist!")

@login_required(login_url='/imagepersona/login/')
def deleteAlbum(request, album_id):
	album = get_object_or_404(ImageFolder, pk = album_id)
	myalbums = request.user.userprofile.albums.all()
	toast = {'display' : 'true', 'message' : 'Album Not Deleted!'}
	albumname = album.name
	if(album in myalbums):
		# Delete album and sub folders
		for subalbum in album.subfolders.all():
			for image in subalbum.images.all():
				image.image.delete(False)
				image.delete()
			if subalbum.croppedDP:
				subalbum.croppedDP.delete(False)
			subalbum.delete()
		album.delete()
		toast["message"] = "Deleted album '" + albumname + "'"
	context = {'toast':toast}
	albums = request.user.userprofile.albums.all()
	if albums is not None:
		context	['albums'] = albums
	return render(request, 'imagepersona/photos.html', context)

@login_required(login_url='/imagepersona/login/')
def downloadAlbum(request, album_id):
	album = get_object_or_404(ImageFolder, pk = album_id)
	if(album in request.user.userprofile.albums.all()):
		s = StringIO.StringIO()
		Zip = zipfile.ZipFile(s, 'w')
		for subalbum in album.subfolders.all():
			subdirpath = str(subalbum.name) + "/"
			for image in subalbum.images.all():
				try:
					Zip.write(image.image.path, subdirpath + os.path.basename(image.image.path))
				except Exception:
					pass
		Zip.close()
		resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
		resp['Content-Disposition'] = 'attachment; filename=%s' % (	str(album.name)+".zip")
		return resp
	return Http404("Not Found!")

@login_required(login_url='/imagepersona/login/')
def deleteSubAlbum(request, album_id, person_id):
	album = get_object_or_404(ImageFolder, pk = album_id)
	person = get_object_or_404(ImageSubFolder, pk = person_id)
	myalbums = request.user.userprofile.albums.all()
	personname = person.name
	albumname = album.name
	toast = {'display' : 'true', 'message' : 'Person Not Deleted!'}
	if(album in myalbums):
		if(person in album.subfolders.all()):
			if person.croppedDP:
				person.croppedDP.delete(False)
			person.delete()
			toast["message"] = "Deleted photos of '" + personname + "' from '" + albumname + "'!"
	return render(request, 'imagepersona/album.html', {'album_name':albumname, 'people':album.subfolders.all(), 'albumPk' : album_id, 'toast':toast})

@login_required(login_url='/imagepersona/login/')
def downloadSubAlbum(request, album_id, person_id):
	album = get_object_or_404(ImageFolder, pk = album_id)
	person = get_object_or_404(ImageSubFolder, pk = person_id)
	if(album in request.user.userprofile.albums.all()):
		if(person in album.subfolders.all()):
			s = StringIO.StringIO()
			Zip = zipfile.ZipFile(s, 'w')
			for image in person.images.all():
				try:
					Zip.write(image.image.path, os.path.basename(image.image.path))
				except Exception:
					pass
			Zip.close()
			resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
			resp['Content-Disposition'] = 'attachment; filename=%s' % (	str(person.name) + "-" + str(album.name) + ".zip")
			return resp
	return Http404("Not Found!")

@login_required(login_url='/imagepersona/login/')
def sharefolder(request, album_id, person_id):
	album = get_object_or_404(ImageFolder, pk = album_id)
	myalbums = request.user.userprofile.albums.all()
	status = request.GET['sharing']
	if(album in myalbums):
		peopleInthisFolder = album.subfolders.all()
		person = get_object_or_404(ImageSubFolder, pk = person_id)
		if(person in peopleInthisFolder):
			about = linksharing.objects.filter(real=person.pk)
			if(len(about) > 0):
				unique_id = about[0].reference
				link_url = "http://" + request.get_host() + '/imagepersona/share/' + unique_id
				if(status != 'undefined'):
					about[0].status = status
				about[0].save()
				return JsonResponse({'Link' : link_url, 'linkStatus' : about[0].status})
			unique_id = get_random_string(length=20)
			# Check whether this string has already been made or not
			link = linksharing()
			link.reference = unique_id
			link.real = person.pk
			link.status = 'true'
			link.save()
			link_url = "http://" + request.get_host() + '/imagepersona/share/' + unique_id
			return JsonResponse({'Link' : link_url, 'linkStatus' : link.status})
	return HttpResponse("hello")

def share(request, unique_id):
	# links = linksharing.all()
	foundlink = get_object_or_404(linksharing, reference = unique_id)
	if(foundlink.status == 'false'):
		raise Http404("Page may have been removed or never existed.")
	person = get_object_or_404(ImageSubFolder, pk = foundlink.real)
	return render(request, 'imagepersona/imagesShared.html', {'images' : person.images.all(), 'PersonName' : person.name})

def verify(request, unique_id):
	ver = get_object_or_404(verifyEmail, reference = unique_id)
	user = ver.user
	user.is_active = True
	user.save()
	return render(request, 'imagepersona/login.html', {'login_error_message': 'Email has been verified!'})

def forgotPasswordRequest(request):
	if request.method == 'POST':
		email = request.POST["email"]
		try:
			user = User.objects.get(email = email)
			unique_id = get_random_string(length=20)
			fp_object, created = forgotPassword.objects.get_or_create(user = user)

			if created:
				fp_object.reference = unique_id
				fp_object.save()
			link_url = "http://" + request.get_host() + '/imagepersona/reset_password/' + fp_object.reference
			send_mail(
				'Account Recovery',
				'Dear ' + user.get_full_name() + ',\n\nClick on this link to reset your password.\n\n' + link_url + '\n\nIf you didn\'t request for password change, please contact us.\n\n--\n\nTeam Image Persona',
				'contact.imagepersona@gmail.com',
				[user.email],
				fail_silently=False,
			)
		except Exception:
			pass
		return render(request, 'imagepersona/forgotPassword.html', {'confirm_message' : True, 'emailid' :email})
	else:
		return render(request, 'imagepersona/forgotPassword.html')

def resetPassword(request, unique_id):
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']
		try:
			user1 = User.objects.get(email=email)
		except Exception:
			return render(request, 'imagepersona/resetPassword.html', {'error' : 'Incorrect Email.',})
		try:
			fp_object = forgotPassword.objects.get(reference = unique_id)
			user2 = fp_object.user
		except Exception:
			return render(request, 'imagepersona/resetPassword.html', {'error' : 'Incorrect Email or the Link has Expired.',})
		if user1 == user2:
			print("Success")
			user1.set_password(password)
			user1.save()
			fp_object.delete()
			return render(request, 'imagepersona/resetPassword.html', {'confirm_message' : True, })
		else:
			return render(request, 'imagepersona/resetPassword.html', {'error' : 'Incorrect Email.',})
	else:
		return render(request, 'imagepersona/resetPassword.html', {})


def ClassifyImages(savedImages, newAlbum, user, host):
	FaceIDs = []
	FaceID_Img_Map = {}
	apicallcount = 0
	wait = True
	if len(APIcalls.objects.all()) <= 0:
		wait = False
	print(user.email)
	while wait:
		latestHit = APIcalls.objects.latest('time')
		now = datetime.utcnow().replace(tzinfo=utc)
		if (latestHit.time - now).total_seconds() < -65 :
			wait = False
		else:
			time.sleep(15)

	for newImage in savedImages:
		if apicallcount >= 20:
			apicallcount = 0
			time.sleep(61)
		apicallcount = apicallcount + 1
		img_url = "http://" + host + newImage.image.url
		body = json.dumps({ 'url': img_url })
		try:
			# Face Detection and retrieving FaceID's
			conn = httplib.HTTPSConnection(settings.CF_BASE_URL)
			conn.request("POST", "/face/v1.0/detect?%s" % CF_detect_params, body, CF_headers)
			response = conn.getresponse()
			data = response.read()
			res = json.loads(data)
			count = len(res)
			# Register API call in databse
			apicall = APIcalls()
			apicall.image = str(apicallcount) + img_url
			apicall.time = datetime.utcnow().replace(tzinfo=utc)
			apicall.save()
			for x in range(0,count):	# For all the people present in the photo
				resx = res[x]["faceId"].encode('ascii')
				FaceIDs.append(resx)
				FaceID_Img_Map[resx] = newImage.pk
			newImage.json_response = data

			# Computer Vision for Tagging
			conn.request("POST", "/vision/v1.0/analyze?%s" % CV_params, body, CV_headers)
			response = conn.getresponse()
			data = response.read()
			res = json.loads(data)
			res = res[u'tags']
			for tag in res:
				if tag["confidence"] > settings.TAG_CONFIDENCE_THRESHHOLD:
					TagObject, created = ImageTag.objects.get_or_create(name=tag["name"].encode("ascii"))
					TagObject.images.add(newImage)
					TagObject.save()
			conn.close()

		except Exception as e:
			return HttpResponse(e)
		newImage.save()

	body = json.dumps({"faceIds" : FaceIDs })
	try:
		conn = httplib.HTTPSConnection(settings.CF_BASE_URL)
		conn.request("POST", "/face/v1.0/group?%s" % CF_group_params, body, CF_headers)
		response = conn.getresponse()
		data = response.read()
		res = json.loads(data)
		conn.close()
	except Exception as e:
		return HttpResponse(e)

	# Grouping people
	res_group = res["groups"]
	for count,personList in enumerate(res_group):
		newPerson = ImageSubFolder()
		newPerson.name = str(count+1)
		newPerson.save()
		flag = True
		for id in personList:
			imgpk = FaceID_Img_Map[id]
			newPerson.images.add(imgpk)
			if flag:
				newPerson.displaypic = imgpk
				newPerson.personid = id
				flag = False
		newPerson.save()
		newAlbum.subfolders.add(newPerson)

	# Messy Images
	newPerson = ImageSubFolder()
	newPerson.name = "Unclassified"
	newPerson.croppedDP.save(str(newAlbum.name) + "-Unclassified.png", unclassified_DP_django_file, save=True)
	newPerson.save()

	for person in newAlbum.subfolders.all():
		for image in person.images.all():
			if image in savedImages:
				savedImages.remove(image)

	for image in savedImages:
		newPerson.images.add(image)

	newAlbum.subfolders.add(newPerson)
	newAlbum.save()

	# Send Completion Mail
	send_mail(
		'Successfully Grouped',
		'Dear ' + str(user.get_full_name()) + ',\n\nYour album ' + str(newAlbum.name) + ' has been processed Completely.\nhttp://' + str(host) + '/imagepersona/album/' + str(newAlbum.pk) + '/\n\n--\nTeam Image Persona',
		'contact.imagepersona@gmail.com',
		[user.email],
		fail_silently=False,
	)
