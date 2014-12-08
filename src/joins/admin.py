from django.contrib import admin

# Register your models here.
from .models import Player
class PlayerAdmin(admin.ModelAdmin):
	list_display = ['username', 'password', 'email', 'timestamp', 'updated' ]
	class Meta:
		model = Player

# from quiz.models import Question
# class QuestionAdmin(admin.ModelAdmin):
				
admin.site.register(Player, PlayerAdmin)
# admin.site.register(Question, QuestionAdmin)