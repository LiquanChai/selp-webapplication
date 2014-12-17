from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.Form):
    """
    The form to register new User
    1. validates that the username is not already in use
    2. password check twice
    """
    required_css_class = 'required'
    username = forms.RegexField(regex=r'^[\w.@+-]+$', 
                                max_length=30, label=_("Username"), 
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    email = forms.EmailField(label=_("E-mail"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
    passwordconfirm = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"))

    def clean_username(self):
        # check username is not already in use
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        # check two password matches or not
        if 'password' in self.cleaned_data and 'passwordconfirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['passwordconfirm']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data