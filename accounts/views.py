from urllib import request
from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import user
from eventproject.utils.jwt_utils import generate_jwt
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def register(request):
    if request.method!='POST':
        return JsonResponse({'error':'Only POST method is allowed'},status=405)
    data=json.loads(request.body)
    username=data.get('username')
    password=data.get('password')
    role=data.get('role')
    if user.objects.filter(username=username).exists():
        return JsonResponse({'error':'Username already exists'},status=400)
    user1=user.objects.create(username=username,password=password,role=role)
    return JsonResponse({
        "message": "User registered successfully",
        "user_id": user1.id
    }, status=201)

@csrf_exempt
def login(request):
    if request.method!='POST':
        return JsonResponse({'error':'Only POST method is allowed'},status=405)
    data=json.loads(request.body)
    username=data.get('username')
    password=data.get('password')
    try:
        user1 = user.objects.get(username=username)
        if user1.password != password:
            return JsonResponse({"error": "Invalid password"}, status=401)
    except user1.DoesNotExist:
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    token = generate_jwt(user1.id,user1.role)
    request.session["last_login"] = user1.username
    request.session["token"] = token
    return JsonResponse({
        "token": token ,
        'role': user1.role
    })

@csrf_exempt
def logout(request):
    request.session.flush()
    return JsonResponse({'message':'Logged out successfully'})
    # Create your views here.

