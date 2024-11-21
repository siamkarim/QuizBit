from django.contrib import admin
from .models import Question, Choice, Practice

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'difficulty', 'created_at')
    list_filter = ('difficulty',)
    search_fields = ('text',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text',)

@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_correct', 'created_at')
    list_filter = ('is_correct',)



