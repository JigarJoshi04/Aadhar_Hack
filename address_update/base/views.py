from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from .decorators import *
import jwt
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import base64
from django.utils.html import strip_tags

#auth
@api_view(['POST'])
def login(request):
	if request.method == 'POST':
		json_data = request.data
		email_id = json_data['email_id']
		password = json_data['password']
		# password hash 
		users = User.objects.filter(email=email_id)
		if not users:
			return Response({'Message':"No user found in the database"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		user = users.first()
		if not user.password == password:
			return Response({'Message':"Wrong password"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		user_id = user.id
		token = get_token_from_object({'user_id':user_id},"_SECRET_KEY")
		user_serializer = UserSerializer([user],many=True)
		return Response({'Message':"User has been logged in",'user':user_serializer.data,'token':token},status=status.HTTP_200_OK)
	else:
		return Response({'Message':"Wrong method"},status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
def register(request):
	if request.method == 'POST':
		# print("ANDAR AAGAYA")
		json_data = request.data
		email_id = json_data['email_id']
		password = json_data['password']
		username = json_data['username']
		# hash password
		users = User.objects.filter(email=email_id)
		if users:
			return Response({'Error':"Email already exists"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		new_user = User(email = email_id,username=username, password = password)
		new_user.save()
		return Response({'Message':"User has been created"},status=status.HTTP_200_OK)
	else:
		return Response({'Error':"Wrong method"},status=status.HTTP_400_BAD_REQUEST)
