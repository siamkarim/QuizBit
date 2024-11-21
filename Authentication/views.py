from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer
)

# Get the user model for the application
User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    View to register a new user.

    This view allows any user (authenticated or not) to register a new account.
    It expects the user data (such as username, email, password) and creates a new user.

    * The user can only POST data to this endpoint.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)  # Allow anyone to access this view
    serializer_class = UserRegistrationSerializer  # Serializer to validate and create a new user

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve and update the authenticated user's profile.

    This view allows an authenticated user to view and modify their own profile.
    It uses the UserSerializer to fetch or update the user details.

    * The user can only GET or PUT data to this endpoint.
    """
    serializer_class = UserSerializer  # Serializer to handle the user's profile data
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can access this view

    def get_object(self):
        """
        Override to return the current authenticated user as the object to be retrieved or updated.
        """
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT token pair.

    This view is a subclass of `TokenObtainPairView` from the `rest_framework_simplejwt` package.
    It allows users to get an access and refresh token pair when they provide valid credentials.

    * The user can only POST to this endpoint with their credentials (username/password).
    """
    serializer_class = CustomTokenObtainPairSerializer  # Custom serializer to handle token generation

class ChangePasswordView(generics.UpdateAPIView):
    """
    View to change the authenticated user's password.

    This view allows an authenticated user to change their password. 
    It expects the new password data and updates the user's password in the database.

    * The user can only PUT data to this endpoint.
    """
    serializer_class = ChangePasswordSerializer  # Serializer to handle password change data
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can change their password

    def get_object(self):
        """
        Override to return the current authenticated user as the object whose password will be changed.
        """
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """
        Handle the update action for changing the password.

        Validates the incoming data, changes the user's password, and then saves the user object.

        Returns a success response on success, or raises an error if validation fails.
        """
        # Validate the incoming data using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Raise an exception if the data is invalid
        
        # Set the new password for the authenticated user and save the user instance
        self.request.user.set_password(serializer.validated_data['new_password'])
        self.request.user.save()
        
        # Return a success response
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
