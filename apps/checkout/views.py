from django.shortcuts import render
from django.http import HttpResponse

def orders(request):
    return HttpResponse('this will be the orders page')
