from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^makan', Makkan.as_view(), name='makan'),
	url(r'^housing', Housing.as_view(), name='housing'),
	
	# url(r'^sample_csv$', sample_csv, name='sample_csv')
]
