from django.conf.urls import url
from . import views

app_name='imagepersona'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^photos/$', views.photos, name='photos'),
    url(r'^profile/$', views.profile, name='profile'),

]
