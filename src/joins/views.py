from django.shortcuts import render, render_to_response,RequestContext,HttpResponseRedirect
from django.contrib import messages
from .forms import RegistrationForm
from time import sleep
def home(request):
 template = "home.html"
 context = {}
 return render(request, template, context)

def signin(request):
 template = "signIn.html"
 context = {}
 return render(request, template, context)
 # return HttpResponseRedirect('/register/')

def register(request):

 form = RegistrationForm(request.POST or None)

 if form.is_valid():
 	save_it = form.save(commit = False)
 	save_it.save()
 	sleep(3)
 	messages.success(request, "Sign up successful!")
 	return HttpResponseRedirect('/signin/')
 else:
 	messages.error(request, "Please enter complete information")

 template = "signUpTest.html"
 context = {"form": form}
 return render_to_response("signuptest.html", locals(), context_instance = RequestContext(request))