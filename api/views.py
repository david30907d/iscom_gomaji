from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.

site = json.load(open('store_to_sites.json', 'r', encoding='utf-8'))
coupon = json.load(open('coupon.json', 'r', encoding='utf-8'))

def getsite(request):
	num = int(request.GET['num']) if 'num' in request.GET else 10
	return JsonResponse(site[:num], safe=False)

def getcoupon(request):
	num = int(request.GET['num']) if 'num' in request.GET else 10
	return JsonResponse(coupon[:num], safe=False)