from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Carousel
from shop.models import Prodotti
# Create your views here.
def index(request):
    slides = Carousel.objects.filter(pubblicato=True,categoria__nome='home')
    return render(request, 'account/home.html', {'slides':slides})

def about(request):
    slides = Carousel.objects.filter(pubblicato=True,categoria__nome='about')
    return render(request,'account/about.html',{'slides':slides})

def contact(request):
    return render(request, 'account/contact.html')








