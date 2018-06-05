from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.

data = json.load(open('store_to_sites.json', 'r', encoding='utf-8'))

def get(request):
	num = int(request.GET['num']) if 'num' in request.GET else 10
	return JsonResponse(data[:num], safe=False)