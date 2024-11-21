from django.db import models
from Authentication.models import User

class Question(models.Model):
    """
    Model to store quiz questions.

    Fields:
        text (TextField): The main content of the question
        created_at (DateTimeField): When the question was created
        updated_at (DateTimeField): When the question was last updated
        difficulty (CharField): Difficulty level of the question (easy/medium/hard)
    """
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Easy'
        MEDIUM = 'medium', 'Medium'
        HARD = 'hard', 'Hard'
    
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM
    )
    
    def __str__(self):
        return f"Question {self.id}: {self.text[:50]}..."

class Choice(models.Model):
    """
    Model to store answer choices for questions.

    Fields:
        question (ForeignKey): Related question
        text (CharField): The text of the choice
        is_correct (BooleanField): Indicates if this is the correct answer
    """
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class Practice(models.Model):
    """
    Model to track user practice sessions.

    Fields:
        user (ForeignKey): The user practicing
        question (ForeignKey): The question being practiced
        selected_choice (ForeignKey): The answer choice selected
        is_correct (BooleanField): Whether the answer was correct
        created_at (DateTimeField): When the practice occurred
    """
    user = models.ForeignKey(User, related_name='practices', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='practices', on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

# Create your models here.
