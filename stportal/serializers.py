from urllib import request
from rest_framework import serializers
from .models import CustomUser,ApplicationModel
from django.contrib.auth.hashers import make_password



class UserSerializers(serializers.ModelSerializer):
    confirm_password=serializers.CharField(max_length=100,style={'input_type': 'password'},write_only=True)
    

    
    class Meta:
        model=CustomUser
        fields=['id','email','first_name','last_name','password','confirm_password','role']
        extra_kwargs = {'password': {'write_only': True,'style':{'input_type': 'password'}}}

    def validate(self, data):
       
        if len(data['first_name'])<3 or len(data['last_name'])<3: 
            raise serializers.ValidationError("Name should be at least 2 character")
        
        if len(data['password'])<5:
            raise serializers.ValidationError("password shoud be at least 6 character")
        
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords should be same") 

        elif data['password'] == data['confirm_password']:
            data['password'] = make_password(data['password'])
            
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return super(UserSerializers, self).create(validated_data)
        
   

class Applicationserializers(serializers.ModelSerializer):
    uni_name=serializers.CharField(max_length=200,min_length=2)
    program_name=serializers.CharField(max_length=200,min_length=5)
   
 
    class Meta:
        model=ApplicationModel
        fields=['uni_name','program_name','study_mode','description']

    

class ApplicationDetailSerializer(serializers.ModelSerializer):
    
    Email=serializers.CharField(source='customer.email')
    first_name=serializers.CharField(source='customer.first_name')
    last_name=serializers.CharField(source='customer.last_name')

    class Meta:
        model=ApplicationModel
        fields=['app_id','Email','first_name','last_name','uni_name','program_name','study_mode','status',]


    def update(self, instance, validated_data): 
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

