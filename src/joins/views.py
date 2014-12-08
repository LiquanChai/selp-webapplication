from django.shortcuts import render, render_to_response,RequestContext,HttpResponseRedirect
from django.contrib import messages
from .forms import RegistrationForm
from time import sleep
from django.core.mail import send_mail
from django.conf import settings

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

 	# send confirm email
 	sbj = 'sign up success at anime quiz!'
 	msg = 'Thank you for join us!'
 	frm = form.cleaned_data['email']
 	to_us = [settings.EMAIL_HOST_USER]
 	send_mail(sbj, msg, frm, to_us, fail_silently=True)
 	#print (sbj,msg,frm,to_us) for debug purpose
 	
 	sleep(3)
 	messages.success(request, "Sign up successful!")
 	return HttpResponseRedirect('/signin/')
 else:
 	messages.error(request, "Please enter complete information")

 template = "signUpTest.html"
 context = {"form": form}
 return render_to_response("signuptest.html", locals(), context_instance = RequestContext(request))