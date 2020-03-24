from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'errand_matcher/index.html')

def signup_volunteer(request):
	return render(request, 'errand_matcher/signup_volunteer.html')