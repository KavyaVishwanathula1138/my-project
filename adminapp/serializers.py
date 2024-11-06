from adminapp.models import Customer,User,Category,FAQ
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth='__all__'



class FAQserrializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class GetFAQserializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
        depth='__all__'
