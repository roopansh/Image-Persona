from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

app_name='imagepersona'

urlpatterns = [
	url(r'^$', RedirectView.as_view(url='upload',permanent=False)),
	url(r'^login/$', views.login_user, name='login'),
	url(r'^register/$', views.register_user, name='register'),
	url(r'^logout/$', views.logout_user, name='logout'),
	url(r'^upload/$', views.upload, name='upload'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^photos/$', views.photos, name='photos'),
	url(r'^album/(?P<album_id>[0-9]+)/$', views.album, name='album'),
	url(r'^images/(?P<album_id>[0-9]+)/(?P<person_id>[0-9]+)/$', views.images, name='images'),
	url(r'^editSubfolder/(?P<album_id>[0-9]+)/(?P<person_id>[0-9]+)/$', views.editSubfolder, name='editSubfolder'),
	url(r'^album/delete/(?P<album_id>[0-9]+)/$', views.deleteAlbum, name='deleteAlbum'),
	url(r'^sharefolder/(?P<album_id>[0-9]+)/(?P<person_id>[0-9]+)/$', views.sharefolder, name='sharefolder'),
]
