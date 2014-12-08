from django.db import models

class Player(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add = True, auto_now=False)
	updated = models.DateTimeField(auto_now_add = False, auto_now=True)
 	
	def __unicode__(self): 
		return "%s" %(self.email)

