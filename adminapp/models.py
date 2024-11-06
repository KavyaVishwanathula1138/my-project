from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token


class User(AbstractUser):
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=30, blank=True, null=True)
	last_name = models.CharField(max_length=30,blank=True, null=True)
	groups = models.ManyToManyField('auth.Group', related_name='user_groups', blank=True)
	user_permissions = models.ManyToManyField('auth.Permission',related_name='user_permissions',blank=True)


class Customer(AbstractUser):
	email = models.EmailField(unique=True)
	name = models.CharField(max_length=30,blank=True, null=True)
	groups = models.ManyToManyField( 'auth.Group',related_name='customer_groups', blank=True)
	user_permissions = models.ManyToManyField('auth.Permission',related_name='customer_permissions', blank=True)
	class Meta:
		verbose_name = 'Customer'
		verbose_name_plural = 'Customers'

	def has_perm(self, perm, obj=None):
		# Custom permission logic here
		if self.is_superuser:
			return True
		if self.user_permissions.filter(codename=perm.split('.')[-1]).exists():
			return True
		return self.groups.filter(permissions__codename=perm.split('.')[-1]).exists()



class UserToken(Token):
	user = models.OneToOneField('adminapp.User', related_name='user_auth_token', on_delete=models.CASCADE)
	class Meta:
		verbose_name = 'UserToken'
		verbose_name_plural = 'UserTokens'



class CustomerToken(Token):
	user = models.OneToOneField('adminapp.Customer',related_name='customer_auth_token', on_delete=models.CASCADE)
	class Meta:
		verbose_name = 'CustomerToken'
		verbose_name_plural = 'CustomerTokens'


class Blog(models.Model):
	content = models.TextField(null= True,blank=True)
	title = models.TextField(null= True,blank=True)

class Category(models.Model):
	category_name = models.CharField(max_length=200,null=True,blank=True)
	category_image= models.ImageField(upload_to='profile_pic', null=True, blank=True)
	description=models.TextField(max_length=300,null=True,blank=True)
	status = models.BooleanField(default=True)
	created_by = models.CharField(max_length=50,null=True,blank=True)
	modified_by = models.CharField(max_length=50,null=True,blank=True)
	category_image_url = models.TextField(blank=True, null=True)




class FAQ(models.Model):
	question = models.TextField(blank=True,null=True)
	answer = models.TextField(blank=True,null=True)
	page_name = models.CharField(max_length=100, blank=True, null=True)
	created_by = models.CharField(max_length=50,null=True,blank=True)
	modified_by = models.CharField(max_length=50,null=True,blank=True)
	status = models.BooleanField(default=True)

	

