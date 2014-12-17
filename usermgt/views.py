from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.http import Http404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
import datetime
import time, string
from usermgt.models import *

# Create your views here.
from django.shortcuts import redirect
from django.views.generic.edit import FormView

import signals
from forms import RegistrationForm


class _RequestPassingFormView(FormView):
    """
    A type of FormView passes (extra) arguments to certain methods, general method
    """
    def get(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        if form.is_valid():
            # Pass request to form_valid.
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def get_form_class(self, request=None):
        return super(_RequestPassingFormView, self).get_form_class()

    def get_form_kwargs(self, request=None, form_class=None):
        return super(_RequestPassingFormView, self).get_form_kwargs()

    def get_initial(self, request=None):
        return super(_RequestPassingFormView, self).get_initial()

    def get_success_url(self, request=None, user=None):
        # constructing success_url need the request and the new user
        return super(_RequestPassingFormView, self).get_success_url()

    def form_valid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_valid(form)

    def form_invalid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_invalid(form)


class RegistrationView(_RequestPassingFormView):
    """
    base class for user registration views.
    
    """
    disallowed_url = 'registration_disallowed'
    form_class = RegistrationForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        # check user sign up is allowed
        if not self.registration_allowed(request):
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, request, form):
        new_user = self.register(request, **form.cleaned_data)
        success_url = self.get_success_url(request, new_user)
         # since success url could be a string or a tuple of arguments
        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def register(self, request, **cleaned_data):
        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
        User.objects.create_user(username, email, password)

        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):

        return True

    def get_success_url(self, request, user):
        return ('/accounts/login/', (), {})





@login_required
def usermgt_profile(request):
    # redirect to userpage
    return HttpResponseRedirect(reverse('quiz_category_list_all'))