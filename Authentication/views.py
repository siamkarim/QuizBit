"""
Authentication Views Module

This module handles user authentication-related operations including:
- User registration
- Profile viewing
- Token generation

The module uses JWT (JSON Web Tokens) for authentication through rest_framework_simplejwt.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    
    POST /api/v1/auth/register/
    
    Request Body:
        {
            "username": string,
            "email": string,
            "password": string,
            "password2": string,
            "first_name": string (optional),
            "last_name": string (optional),
            "phone_number": string (optional),
            "gender": string (optional),
            "date_of_birth": date (optional),
            "bio": string (optional)
        }
    
    Returns:
        201 Created - On successful registration
        {
            "status": "success",
            "user": {
                "id": int,
                "username": string,
                "email": string,
                "first_name": string,
                "last_name": string
            },
            "tokens": {
                "refresh": string,
                "access": string
            }
        }
        
        400 Bad Request - On validation errors
        {
            "field_name": [
                "error message"
            ]
        }
    """
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.
        
        Creates a new user account and returns user data with authentication tokens.
        Performs validation on the input data using UserRegistrationSerializer.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    API endpoint for viewing and updating user profile.
    
    GET /api/v1/auth/profile/
    
    Authentication:
        Required - JWT Token in Authorization header
        
    Returns:
        200 OK
        {
            "id": int,
            "username": string,
            "email": string,
            "first_name": string,
            "last_name": string,
            "phone_number": string,
            "gender": string,
            "date_of_birth": date,
            "bio": string
        }
        
        401 Unauthorized - If not authenticated
        
    Notes:
        - Returns the complete profile of the authenticated user
        - Sensitive fields like password are never returned
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests for user profile.
        
        Returns the complete profile information of the authenticated user.
        """
        user = request.user
        serializer = UserRegistrationSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    


