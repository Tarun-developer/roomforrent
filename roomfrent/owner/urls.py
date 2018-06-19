from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
	# url(r'^$', Dashboard.as_view(), name='dashboard'),
	# url(r'^sample_csv$', sample_csv, name='sample_csv')
    url(r'^$',OwnerDashboard.as_view(),name='owner_dashboard'),
    url(r'^owner_profile',OwnerProfile.as_view(),name='owner_profile'),
    url(r'^owner_property',OwnerProperty.as_view(),name='owner_property'),
    url(r'^register',OwnerRegister.as_view(),name='register'),
    url(r'^owner_add_property',OwnerAddProperty.as_view(),name='owner_add_property'),
    url(r'^register', login_required(OwnerRegister.as_view())),
    url(r'^logout/$', OwnerRegister.logout_view),




]
