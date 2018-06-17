from django.db import models

# Create your models here.
class Furnish(models.Model):
	fully = models.IntegerField(blank=True,null=True,default=0)
	partially= models.IntegerField(blank=True,null=True,default=0)
	unfurnished= models.IntegerField(blank=True,null=True,default=0)

	
	def __str__(self):
		return str(self.id)

class Apartment(models.Model):
	name=models.CharField(max_length=500,null=True,blank=True)
	def __str__(self):
		return str(self.id)



class BHK(models.Model):
	name=models.CharField(max_length=500,null=True,blank=True)
	def __str__(self):
		return str(self.id)
class Preference(models.Model):
	family = models.IntegerField(blank=True,null=True,default=0)
	girls= models.IntegerField(blank=True,null=True,default=0)
	bachelor= models.IntegerField(blank=True,null=True,default=0)
	def __str__(self):
		return str(self.id)

class Images(models.Model):
	name=models.CharField(max_length=500,null=True,blank=True)
	def __str__(self):
		return str(self.name)
		
class OwnerInfo(models.Model):
	name = models.CharField(max_length = 100)
	owner_password = models.CharField(max_length = 200)
	owner_mobile = models.CharField(max_length = 10)
	email = models.CharField(max_length = 100)
	# propertie=models.ForeignKey(Property,on_delete=models.CASCADE,blank=True,null=True)

	def __str__(self):
		return str(self.owner_mobile)
class Property(models.Model):
	name=models.CharField(max_length=500)
	owner = models.ForeignKey(OwnerInfo,on_delete=models.CASCADE)
	location = models.CharField(max_length=1000)	
	status = models.IntegerField(blank=True,null=True,default=1)
	rating = models.IntegerField(blank=True,null=True,default=5)
	created_at = models.DateField(blank=True,null=True)
	budget=models.CharField(blank=True,null=True,max_length=500)
	apartment=models.ForeignKey(Apartment,on_delete=models.CASCADE,blank=True,null=True)
	furnish=models.ForeignKey(Furnish,on_delete=models.CASCADE,blank=True,null=True)
	bhk=models.ForeignKey(BHK,on_delete=models.CASCADE,blank=True,null=True)
	preference=models.ForeignKey(Preference,on_delete=models.CASCADE,blank=True,null=True)
	image=models.ForeignKey(Images,on_delete=models.CASCADE,blank=True,null=True)
	lat=models.FloatField(blank=True,null=True)
	lng=models.FloatField(blank=True,null=True)


		
	def __str__(self):
		return str(str(self.name)+'  '+str(self.location))


class Client(models.Model):
	name = models.CharField(max_length = 100)
	email = models.EmailField()
	mobile = models.CharField(max_length = 100)
	addhar = models.CharField(max_length = 15)
	def __str__(self):
		return str(self.name)

class ClientReivew(models.Model):
	client = models.ForeignKey(Client,on_delete=models.CASCADE)
	owner = models.ForeignKey(OwnerInfo,on_delete=models.CASCADE)
	review = models.IntegerField(null=True,blank=True)
	comment = models.CharField(max_length=200,null=True,blank=True)
	

	def __str__(self):
		return str(self.id)