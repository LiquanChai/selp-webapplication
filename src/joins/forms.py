from .models import Player
from django import forms

class RegistrationForm(forms.ModelForm):
	class Meta: 
		model = Player 
		fields = ["username", "password", "email",] 
