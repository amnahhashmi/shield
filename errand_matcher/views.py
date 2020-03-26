from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'errand_matcher/index.html')

def begin_signup(request):
	return render(request, 'errand_matcher/begin-signup.html')

def matchable_volunteers(request, requestor_id):
	pass
