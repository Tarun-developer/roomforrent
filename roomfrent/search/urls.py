from django.conf.urls import url
from .views import HomePage,SearchResults

urlpatterns = [
	url(r'^$', HomePage.as_view(), name='homepage'),
	# url(r'^sample_csv$', sample_csv, name='sample_csv')
        url(r'^search_results',SearchResults.as_view(),name='search_results'),
]
