from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Question, Choice, Practice
from .serializers import (
    QuestionListSerializer, 
    QuestionDetailSerializer,
    AnswerSubmissionSerializer,
    PracticeHistorySerializer
)

class QuestionListView(generics.ListAPIView):
    """
    API endpoint that allows viewing a list of questions.
    
    GET /api/v1/quiz/questions/
    
    Query Parameters:
        difficulty (optional): Filter questions by difficulty level
            Values: 'easy', 'medium', 'hard'
            
    Returns:
        List of questions with basic information:
        - id
        - text
        - difficulty
        - created_at
    
    Example:
        GET /api/v1/quiz/questions/?difficulty=easy
    """
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer
    
    def get_queryset(self):
        """
        Optionally filters questions by difficulty level from query parameters.
        """
        queryset = Question.objects.all()
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset

class QuestionDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows viewing detailed information about a specific question.
    
    GET /api/v1/quiz/questions/{id}/
    
    Returns:
        Detailed question information including:
        - id
        - text
        - difficulty
        - choices
        - created_at
    
    Raises:
        404: If question with given ID does not exist
    """
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer

class AnswerSubmissionView(generics.CreateAPIView):
    """
    API endpoint for submitting answers to questions.
    
    POST /api/v1/quiz/questions/{id}/submit/
    
    Authentication:
        Required
    
    Request Body:
        {
            "choice_id": int
        }
    
    Returns:
        {
            "is_correct": boolean,
            "message": string
        }
    
    Raises:
        400: If choice does not belong to the question
        401: If user is not authenticated
        404: If question or choice not found
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerSubmissionSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new practice attempt.
        
        Validates that:
        1. The choice exists
        2. The choice belongs to the question
        3. Creates a practice record
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        question = get_object_or_404(Question, pk=kwargs['pk'])
        choice = get_object_or_404(Choice, pk=serializer.validated_data['choice_id'])
        
        if choice.question_id != question.id:
            return Response(
                {'error': 'Choice does not belong to this question'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        practice = Practice.objects.create(
            user=request.user,
            question=question,
            selected_choice=choice,
            is_correct=choice.is_correct
        )
        
        return Response({
            'is_correct': practice.is_correct,
            'message': 'Answer submitted successfully'
        })

class PracticeHistoryView(generics.ListAPIView):
    """
    API endpoint that allows users to view their practice history.
    
    GET /api/v1/quiz/practice-history/
    
    Authentication:
        Required
    
    Returns:
        List of practice attempts including:
        - id
        - question details
        - selected choice
        - correctness
        - timestamp
    
    Notes:
        - Only returns practice history for the authenticated user
        - Ordered by most recent first
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PracticeHistorySerializer
    
    def get_queryset(self):
        """
        Returns practice history for the authenticated user only.
        """
        return Practice.objects.filter(user=self.request.user)

