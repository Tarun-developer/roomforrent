from django.shortcuts import render

# Create your views here.
import base64
import csv
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.contrib import messages
# from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import json,pprint
from django.views.decorators.csrf import csrf_exempt
from . import models
from passlib.hash import django_pbkdf2_sha256 as handler
import pytz
from random import randint
import requests
from django.db import connection
from django.core import serializers
import json
# google map api
import googlemaps
from datetime import datetime
gmaps = googlemaps.Client(key='AIzaSyCn4KrK85eV6WY_E9KC460feVjSukKlLsw')

# from login.models import *
utc = pytz.UTC


    # ADMIN



class HomePage(TemplateView):
    template_name = "dashboard.html"


    def get_context_data(self, * args, ** kwargs):
        context = super(HomePage, self).get_context_data()
        self.request.environ['REMOTE_ADDR']
        # if  self.request.environ['REMOTE_ADDR'] == '127.0.0.1':
        #     context['ip'] = '27.255.211.216'
        # else:
        #     context['ip'] = self.request.environ['REMOTE_ADDR']
        # g = GeoIP2()
        # location_data = g.city(context['ip'])
        # # city = g.city('106.192.73.120')
        # context['city'] = location_data['city']
        # context['country'] = location_data['country_name']


        # return context
	
    # 

class SearchResults(TemplateView):
    template_name = "search_results.html"
    def get_context_data(self, * args, ** kwargs):
        context = super(SearchResults, self).get_context_data()
        search_result = self.request.GET.get('search')
        # database_result = Property.objects.filter(location=search_result)
        # g = googlemap(search_result)
        # print nearby_place
        context['search_result'] = search_result
        return context
    def post(self, request):
        # print request.POST
        search_result = request.POST.get('search_query')
        # print search_result
        result_add_query = gmaps.places(search_result)
        # print result_add_query
        lat=result_add_query['results'][0]['geometry']['location']['lat']
        lng=result_add_query['results'][0]['geometry']['location']['lng']
        cursor = connection.cursor()
        query='SELECT id,( 6371 * acos(cos(radians('+str(lat)+'))* cos(radians(lat)) * cos(radians(lng) - radians('+str(lng)+')) + sin(radians('+str(lat)+')) * sin(radians(lat )))) AS distance_KM ,location,name FROM search_property HAVING distance_KM >= 0 ORDER BY distance_KM '
        # print query
        # cursor.execute('''SELECT id,( 6371 * acos(cos(radians(lat)) * cos(radians(lat)) * cos(radians(lng) - radians(77.5612252)) + sin(radians(28.4581258)) * sin(radians(lat )))) AS distance_KM FROM search_property HAVING distance_KM > 50 ORDER BY distance_KM LIMIT 0, 20;''')
        # result_set = dictfetchall(cursor)
        all_results=[]
        all_property=Property.objects.raw(query)

        json={}
        for i in all_property:
            json={}
            json['id']=str(i.id)
            json['name']=str(i.name)
            json['distance']=str(i.distance_KM)
            json['image']=str(i.image)
            json['budget']=str(i.budget)
            json['image']=str(i.image)
            json['location']=str(i.location)
            json['owner']=str(i.owner.name)
            json['owner_mob']=str(i.owner.owner_mobile)
            json['furnish']=str(i.furnish_id)


            all_results.append(json)
        # return HttpResponse(all_results)
           
            # p_id = (i.id)
            # distance['++'] = (i.distance_KM)
            # # print p_id
            # database_result = Property.objects.filter(id=p_id)
            # print database_result
        return JsonResponse(all_results, safe=False)
        




       