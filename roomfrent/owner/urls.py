from django.conf.urls import url
from .views import *

urlpatterns = [
	# url(r'^$', Dashboard.as_view(), name='dashboard'),
	# url(r'^sample_csv$', sample_csv, name='sample_csv')
    url(r'^$',OwnerDashboard.as_view(),name='owner_dashboard'),
    url(r'^owner_profile',OwnerProfile.as_view(),name='owner_profile'),
    url(r'^owner_property',OwnerProperty.as_view(),name='owner_property'),
    url(r'^owner_register',OwnerRegister.as_view(),name='owner_register'),
    url(r'^owner_add_property',OwnerAddProperty.as_view(),name='owner_add_property'),





]
