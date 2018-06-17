from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
import requests
import json
from .models import *
from datetime import datetime,timedelta
from django.db.models import Q
from django.utils.decorators import method_decorator
import csv
import base64
from passlib.hash import django_pbkdf2_sha256 as handler
from random import randint
from django.conf import settings
import pytz
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response
from django.contrib import messages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import requests,time
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
utc=pytz.UTC
from search.models import *


					# ADMIN



class Makkan(TemplateView):
	template_name = "dashboard.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(Makkan, self).dispatch(request, *args, **kwargs)



	def get_context_data(self, *args, **kwargs):
		context = super(Makkan, self).get_context_data()
		
		
		return context
	def post(self,request):
		# nearby_place = gmaps.places_nearby('30.6452228,76.6368483',5000, None,None, None, None, None,False, None,'locality',None)
		# places_add = gmaps.places_radar('30.6452228,76.6368483', None, 5000,None, None, None,None)
		# pprint.pprint(places_add)
		# for i in nearby_place['results']:
		# 	pprint.pprint(i['vicinity'])
		# 	location_name =i['name']

		html=requests.get('https://www.makaan.com/listings?postedBy=owner&listingType=rent&pageType=CITY_URLS&cityName=Chandigarh&cityId=24&templateId=MAKAAN_CITY_LISTING_RENT')
		soup = BeautifulSoup(html.text, 'html.parser')
		# print (soup)
		final_property_links=[]
		all_links=soup.find_all('div',{'class':'infoWrap'})
		for link in all_links:
			a_tags=link.find('a')
			final_property_links.append((a_tags['href']))

		print ('\n\n **************************************888')
		
		driver = webdriver.Chrome(settings.CHROMEDRIVER_PATH)
		driver.set_window_size(1700, 700)
		records = []

		all_properties=[]
		for counter,page in enumerate(final_property_links):
			try:
				
				print (' WROTE '+str(counter)+' out of '+str(len(final_property_links)))
				json={}
				driver.get(page)
				data={}
				if counter == 0:
					time.sleep(5)
				else:
					time.sleep(9)
					elemt=driver.find_element_by_class_name('txtlink')
					driver.execute_script("arguments[0].scrollIntoView();", elemt)
					time.sleep(3)
					elemt.click()
					time.sleep(3)
					print ('999')
					phone=driver.find_element_by_class_name('see-phoneno')
					title=driver.find_element_by_xpath("//div[@class='type-col']//span[@class='type']")
					location1=driver.find_element_by_class_name('loc-name')
					location2=driver.find_element_by_class_name('city-name')
					location=(location1.text)+' '+str(location2.text)
					price=driver.find_element_by_xpath("//div[@class='price-wrap']//span")
					bhk=driver.find_element_by_xpath("//div[@class='type-col']//span[@itemprop='name']")
					bhk=bhk.text
					bhk=bhk.split('BHK')
					bhk=bhk[0]
					

					table=driver.find_element_by_xpath("//table[@class='sub-points']//td[@id='Status']")
					if table.text =='Furnished':
						status=1
					if table.text =='Semi-Furnished':
						status=2
					
					image_list=[]
					all_images=driver.find_elements_by_class_name("imgzoom")
					for image in all_images:
						src=image.find_element_by_tag_name('img').get_attribute("data-src")
						image_list.append(str(src))
					
					json['phone'],json['title'],json['location'],json['price'],json['status'],json['bhk'],json['image_list']=str(phone.text),str(title.text),str(location),str(price.text),status,bhk,image_list
					all_properties.append(json)
					print (all_properties)
					
					print('\n')
					# breakowner_name
			except Exception as r:
				print (r)
				pass
		
		print ('\n\n\n')
		print ('writing to db')
		for i,lis in enumerate(all_properties):
			try:
				address = lis['location']
				result_add_query = gmaps.places(address)
				lat=result_add_query['results'][0]['geometry']['location']['lat']
				lng=result_add_query['results'][0]['geometry']['location']['lng']
				older_property=Property.objects.filter(name=lis['title'],budget=str(lis['price']),location=lis['location'])
				print ('ssssssssss')
				if not older_property:
					myString = ",".join(lis['image_list'] )
					image_obj=Images.objects.create(name=myString)

					if lis['status']==1:
						furn_obj=Furnish.objects.create(fully=1)
					if lis['status']==2:
						furn_obj=Furnish.objects.create(partially=1)

					bhk_obj=BHK.objects.create(name=lis['bhk'])
					new_property=Property.objects.create(name=lis['title'],location=lis['location'],status=1,budget=str(lis['price']),furnish=furn_obj,bhk=bhk_obj,image=image_obj,lat=lat,lng=lng)
					

				image_obj=''
				myString=''
			except Exception as rr:
				print (rr)

		return  HttpResponse('1')






class Housing(TemplateView):
	template_name = "dashboard.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(Housing, self).dispatch(request, *args, **kwargs)



	def get_context_data(self, *args, **kwargs):
		context = super(Housing, self).get_context_data()
		
		
		return context
	def post(self,request):
		url=('http://www.propertybazaar.com/Real-estate-properties-residential-apartment-for-rent-in-gurgaon.html')
		browser = webdriver.Chrome(settings.CHROMEDRIVER_PATH)
		browser.set_window_size(1700, 700)
		records = []



		
		profile_obj=browser.get('http://www.propertybazaar.com/Real-estate-properties-independent-house-villa-for-sale-in-dwarkadelhi.html')
		time.sleep(4)
		change_dropdown=browser.find_elements_by_class_name('changetype')
		change_dropdown[1].click()
		time.sleep(2)
		select_box=browser.find_element_by_id("DropSearchPropTransType")
		select = Select(select_box)
	
		try:
			select.select_by_value('2')
		except Exception as e:
				# fail the Test if the element can not be found or timeout occurs
			print('Test failed, the flight class drop down could not be found ')
		time.sleep(20)
		all_tables=browser.find_elements_by_class_name("Example")
		all_properties=[]


		for counter,table in enumerate(all_tables):
			print (' WROTE '+str(counter)+' out of '+str(len(all_tables)))
			
			try:
				json={}
				date_div=table.find_elements_by_id('inertbl')
				date=date_div[1].text
				date=date.split('on:')
				date=(date[1])
			except:
				date=''

			print (date)
			try:
				property_title=table.find_element_by_id("result_protype").text
			except:
				property_title=''
			print (property_title)
			try:
				area=table.find_element_by_class_name('secondatt')
				print (area.text)
			except:
				area=''
			table.find_element_by_id("cont_btn").click()
			try:
				username=browser.find_element_by_id('username')
				username=username.text
			except:
				username=''
			try:

				phone=browser.find_element_by_id("phone")
				phone= (phone.text)
				
			except:
				phone=''

			close_popup=browser.find_elements_by_class_name('ui-dialog-titlebar-close')
			close_popup[4].click()
			time.sleep(2)
			json['phone'],json['title'],json['location'],json['price'],json['status'],json['image_list'],json['username']=str(phone),str(property_title),str(property_title),str('On Request'),1,'',username
			all_properties.append(json)
			print (all_properties)
			print ('\n')





		for i,lis in enumerate(all_properties):
			try:

				older_property=Property.objects.filter(name=lis['title'],budget=str(lis['price']),location=lis['location'])
				print ('ssssssssss')
				if not older_property:
					
					if lis['status']==1:
						furn_obj=Furnish.objects.create(fully=1)
					if lis['status']==2:
						furn_obj=Furnish.objects.create(partially=1)

					
					new_property=Property.objects.create(name=lis['title'],location=lis['location'],status=1,budget=str(lis['price']),furnish=furn_obj)

					new_owner=OwnerInfo.objects.create(name=lis['username'],owner_mobile=lis['phone'],propertie=new_property)
					

				new_property=''
				mew_owner=''
				
			except Exception as rr:
				print (rr)

		return  HttpResponse('1')


