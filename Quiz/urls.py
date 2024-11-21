from django.urls import path
from .views import (
    QuestionListView,
    QuestionDetailView,
    AnswerSubmissionView,
    PracticeHistoryView
)

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:pk>/submit/', AnswerSubmissionView.as_view(), name='submit-answer'),
    path('practice-history/', PracticeHistoryView.as_view(), name='practice-history'),
]