from rest_framework import serializers
from .models import Question, Choice, Practice

class ChoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for Choice model.
    
    Fields:
        id (int): The unique identifier of the choice
        text (str): The text content of the choice
    """
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Questions with basic information.
    
    Fields:
        id (int): The unique identifier of the question
        text (str): The question text
        difficulty (str): Difficulty level of the question
        created_at (datetime): When the question was created
    """
    class Meta:
        model = Question
        fields = ['id', 'text', 'difficulty', 'created_at']

class QuestionDetailSerializer(serializers.ModelSerializer):
    """
    Detailed Question serializer including associated choices.
    
    Fields:
        id (int): The unique identifier of the question
        text (str): The question text
        difficulty (str): Difficulty level of the question
        choices (list): List of associated choices using ChoiceSerializer
        created_at (datetime): When the question was created
    """
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'difficulty', 'choices', 'created_at']

class AnswerSubmissionSerializer(serializers.Serializer):
    """
    Serializer for submitting answers to questions.
    
    Fields:
        choice_id (int): The ID of the selected choice
        
    Used for validating answer submissions in the quiz system.
    """
    choice_id = serializers.IntegerField()

class PracticeHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for user's practice history.
    
    Fields:
        id (int): The unique identifier of the practice attempt
        question (dict): The associated question details
        selected_choice (dict): The user's selected choice
        is_correct (bool): Whether the answer was correct
        created_at (datetime): When the practice attempt was made
        
    Includes nested serializers:
        - QuestionListSerializer for question details
        - ChoiceSerializer for selected choice
    """
    question = QuestionListSerializer()
    selected_choice = ChoiceSerializer()
    
    class Meta:
        model = Practice
        fields = ['id', 'question', 'selected_choice', 'is_correct', 'created_at']
