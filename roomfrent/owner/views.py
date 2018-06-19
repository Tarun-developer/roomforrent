from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from search.models import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
import json,pprint
from django.core import serializers
# from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyCn4KrK85eV6WY_E9KC460feVjSukKlLsw')


# Create your views here.
class LoggedInMixin(object):
    @method_decorator(login_required(login_url='/owner/register/'))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)

class OwnerDashboard(LoggedInMixin,TemplateView):
    template_name = "owner_dashboard.html"

    def get_context_data(self, * args, ** kwargs):
        context = super(OwnerDashboard, self).get_context_data()
        return context

class OwnerProfile(LoggedInMixin,TemplateView):
    template_name = "owner_profile.html"

    def get_context_data(self, * args, ** kwargs):
        context = super(OwnerProfile, self).get_context_data()
        

        return context

class OwnerProperty(LoggedInMixin,TemplateView):
    template_name = "owner_property.html"

    def get_context_data(self, * args, ** kwargs):
        context = super(OwnerProperty, self).get_context_data()
        owner=self.request.user.id
        all_prop=list(Property.objects.filter(owner_id=(owner)))
        context['propertys'] = all_prop


        return context

class OwnerRegister(TemplateView):
    template_name = "owner_register.html"

    def get_context_data(self, * args, ** kwargs):
        context = super(OwnerRegister, self).get_context_data()
        return context
    def logout_view(request):
        logout(request)
        return HttpResponseRedirect("/")

    def post(self, request):
        islogin = request.POST.get('islogin')
        password = request.POST.get('password')
        mobile = request.POST.get('moblie')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')


        if islogin:

            try:
                user = authenticate(username=mobile, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                      
                        return HttpResponseRedirect("/owner/?own=" + str(user.id))
                else:
                    messages.info(request,'invalid password. please try again')
                    return HttpResponseRedirect("/owner/register")
            except Exception as r:
                  messages.info(request,'invalid password. please try again')
                  return HttpResponseRedirect("/owner/register")
        else:
            try:
                owner_obj = OwnerInfo.objects.get(owner_mobile=mobile)
                if owner_obj:
                    messages.info(request,'please login at your right')
                    return HttpResponseRedirect("/owner/register")
            
            except Exception as r:
                user=User.objects.create_user(mobile, email, password)
                user.first_name = first_name
                user.save()
                owner_register = OwnerInfo(user=user,owner_mobile=mobile)
                owner_register.save()
                user = authenticate(username=mobile, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect("/owner/owner_add_property/?own=" + str(user.id))

class OwnerAddProperty(LoggedInMixin,TemplateView):
    template_name = "owner_add_property.html"

    def get_context_data(self, * args, ** kwargs):
        context = super(OwnerAddProperty, self).get_context_data()
        return context
    def post(self, request):

        try:
            property_type = request.POST.get('property_type')
            property_status = request.POST.get('property_status')
            loaction = request.POST.get('loaction')
            price = request.POST.get('price')
            city = request.POST.get('city')
            family = request.POST.getlist('checks[]')
            # print(family)
            # if family[0]==1:
            #     pref_obj=Preference.objects.create(family=1,girls=1,bachelor=1)
            # if family[0]==2:
            #     pref_obj=Preference.objects.create(family=1,girls=1,bachelor=1)
            #     if family=='3':
            # if property_status=='Furnished':
            #     pref_obj=Preference.objects.create(family=1)
            # if property_status=='Furnished':
            #     pref_obj=Preference.objects.create(girls=1)
            # if property_status=='Furnished':
            pref_obj=Preference.objects.create(bachelor=1)
       
            bachelor = request.POST.get('bachelor')
            girls = request.POST.get('girls')
            result_add_query = gmaps.places(loaction)
            print(request.user.id)
            lat=result_add_query['results'][0]['geometry']['location']['lat']
            lng=result_add_query['results'][0]['geometry']['location']['lng']
            if property_status=='Furnished':
                furn_obj=Furnish.objects.create(fully=1)
            if property_status=='Semi Furnished':
                furn_obj=Furnish.objects.create(partially=1)
            if property_status=='Unfurnished':
                furn_obj=Furnish.objects.create(unfurnished=1)
            new_property=Property.objects.create(name=str(property_type) +str(" - ")+ str(property_status),created_at=timezone.now() ,location=loaction,status=1,budget=price,furnish=furn_obj,preference=pref_obj,lat=lat,lng=lng,owner_id=request.user.id)
        except Exception as rr:
                print (rr)

        return HttpResponseRedirect("/owner/owner_property")