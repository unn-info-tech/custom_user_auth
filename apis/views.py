from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import UserRegistrationSerializer, UserLoginSerializer, VerifyOTPSerializer

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .tasks import send_otp_email, generate_and_store_otp
from django.core.exceptions import ObjectDoesNotExist
import time
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# REGISTER
@swagger_auto_schema(
    method='post',
    request_body=UserRegistrationSerializer,
    responses={
        status.HTTP_201_CREATED: UserRegistrationSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    operation_summary="**Register a new user**",
    operation_description="**Create a new user account by providing the required information.**\n"
                          "To register a new user:\n"
                          "1. Click the 'Try it out' button.\n"
                          "2. Fill out the request body with required user details in the 'Request Body' section.\n"
                          "3. Click the 'Execute' button to send the registration request.\n"
                          "4. If the provided information is valid and the email is not already registered,\n"
                          "   a new user account will be created and the user details will be returned.\n"
                          "5. If the email is already registered, an error response will be returned.\n"
                          "6. Check the response status code and message to determine the outcome.",
)
@api_view(['POST'])
def register_user(request):
    """
    Register a new user.

    Create a new user account by providing the required information.

    :param request: The request object.
    :return: A Response containing user details if successful, or an error response.
    """
    
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password with Argon2 using make_password
            hashed_password = make_password(serializer.validated_data['password'])
            
            # Check if the email is already registered
            email = serializer.validated_data['email']
            if CustomUser.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save(password=hashed_password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# LOGIN
@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,
    responses={
        status.HTTP_200_OK: "Successfully logged in",
        status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        status.HTTP_404_NOT_FOUND: "User not found",
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    operation_summary="**User Login**",
    operation_description="**Log in a user by providing their email and password.**\n"
                          "To log in and obtain an authentication token:\n"
                          "1. Click the 'Try it out' button.\n"
                          "2. Fill out the request body with your registered email and password.\n"
                          "3. Click the 'Execute' button to retrieve the response.\n"
                          "   If the provided credentials are valid, an OTP will be generated and sent to your registered email address.\n"
                          "   Additionally, the OTP will be displayed in the terminal for testing purposes.\n"
                          "5. Proceed to the 'Verify OTP' API endpoint and complete the request body by entering the OTP you received in your email(or printed in the terminal).\n"
                          "   **Please note that the OTP is valid for a duration of 2 minutes.**"
                          
)
@api_view(['POST'])
def user_login(request):
    """
    User Login.

    Log in a user by providing their email and password.

    :param request: The request object.
    :return: A Response containing success message or error response.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = CustomUser.objects.filter(email=email).first()
        if user:
            if user.check_password(password):
                # Generate and send OTP

                # this is for test which will be printed in the terminal,
                # you can work even without config. celery
                generated_test_otp = generate_and_store_otp(user.email) 
                print('This is otp for test:', generated_test_otp)

                # this one is for celery

                send_otp_email(user.email, generated_test_otp)
                
                

                # Store the values in the session for later validation
                request.session['generated_test_otp'] = generated_test_otp
                request.session['user_id'] = user.id
                
                return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Verify OTP 
@swagger_auto_schema(
    method='post',
    request_body=VerifyOTPSerializer,
    responses={
        status.HTTP_200_OK: "OTP verified and token issued",
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "User not found",
    },
    operation_summary="**Verify OTP**",
    operation_description="""**Verify the provided OTP and issue a token if the OTP is valid.**
                          To verify the OTP and obtain an authentication token:
                          1. Click the 'Try it out' button.
                          2. Fill out the request body with OTP you received after verifying your email.
                             (In case the email functionality is not working, the OTP will be printed in the terminal for testing purposes).
                          3. Click the 'Execute' button to retrieve the response.
                          4. If the OTP is valid, an authentication token will be issued.
                          5. Use the issued token in the 'Authorization' header for subsequent requests.""",
)
@api_view(['POST'])
def verify_otp(request):
    """
    Verify OTP .

    Verify the provided OTP against the cached OTP and issue a token if the OTP is valid.

    :param request: The request object.
    :return: A Response containing success message or error response.
    """
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        input_otp = serializer.validated_data['otp']
        user_id = request.session.get('user_id')

        try:
            user = CustomUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the cached OTP and timestamp
        cache_key = f"otp_{user.email}"  # Use the user's email as the cache key
        cached_data = cache.get(cache_key)
        if cached_data is None:
            return Response({'error': 'OTP expired or not generated'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(cached_data)
        cached_otp = cached_data.get('otp')
        cached_timestamp = cached_data.get('timestamp')
        
        # Check if the provided OTP matches the cached OTP
        if input_otp == cached_otp:
            # Check if OTP has expired
            current_timestamp = int(time.time())
            expiration_time = 60  # OTP expires in 2 minutes (120 seconds)
            if current_timestamp - cached_timestamp <= expiration_time:
                # OTP is valid and within the expiration time
                token, _ = Token.objects.get_or_create(user=user)

                # Remove the OTP data from the cache to prevent reusing
                cache.delete(cache_key)

                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#PROFILE
@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: "User profile retrieved successfully",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    },
    operation_summary="**User Profile**",
    operation_description="""**Retrieve the user's profile information.**
    1.Click the 'Try it out' button.
    2.Enter the authentication token you obtained after verifying the OTP into the 'Authorization' field.
    Example: Token 'your_token' followed by a space(Token 2a16f6b6cfa1f84b647bba8ea45b3ab11a7b3b93).
    3. Click the 'Execute' button to retrieve the response.""",
    manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token", type=openapi.TYPE_STRING),
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    User Profile.

    Retrieve the user's profile information.

    :param request: The request object.
    :return: A Response containing the user's profile data or error response.
    """
    try:
        user = request.user
        profile_data = {
            'username': user.username,
            'email': user.email,
        }
        return Response(profile_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#UPDATE
@swagger_auto_schema(
    methods=['patch'],
    request_body=UserRegistrationSerializer,
    responses={
        status.HTTP_200_OK: "Profile updated successfully",
        status.HTTP_400_BAD_REQUEST: "Bad request or validation error",
        status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    },
    operation_summary="**Update User Profile**",
    operation_description="""**Update the user's profile information.**
    1.Click the 'Try it out' button.
    2.Enter the authentication token you obtained after verifying the OTP into the 'Authorization' field.
    Example: Token 'your_token' followed by a space(Token 2a16f6b6cfa1f84b647bba8ea45b3ab11a7b3b93).
    3. Fill out the request body with the new user profile information.
    4. Click the 'Execute' button to retrieve the response.""",
    manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token", type=openapi.TYPE_STRING),
    ]
)
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update User Profile.

    Update the user's profile information.

    :param request: The request object.
    :return: A Response indicating the success of the update or an error response.
    """
    user = request.user
    serializer = UserRegistrationSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        hashed_password = make_password(serializer.validated_data['password'])
        user = serializer.save(password=hashed_password)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# LOGOUT
@swagger_auto_schema(
    method='post',
    responses={
        status.HTTP_200_OK: "Successfully logged out",
        status.HTTP_400_BAD_REQUEST: "Token not found or bad request",
        status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    },
    operation_summary="**User Logout**",
    operation_description="""**Logout the currently authenticated user.**
    1.Click the 'Try it out' button.
    2.Enter the authentication token you obtained after verifying the OTP into the 'Authorization' field.
    Example: Token 'your_token' followed by a space(Token 2a16f6b6cfa1f84b647bba8ea45b3ab11a7b3b93).
    3. Click the 'Execute' button to retrieve the response.""",

    
    manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token", type=openapi.TYPE_STRING),
    ]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    User Logout.

    Logout the currently authenticated user.

    :param request: The request object.
    :return: A Response indicating the success of the logout or an error response.
    """
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found. Already logged out.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred while logging out.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# DELETE
@swagger_auto_schema(
    method='delete',
    responses={
        status.HTTP_204_NO_CONTENT: "User deleted successfully",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    },
    operation_summary="**Delete User**",
    operation_description="""**Logout the currently authenticated user.**
    1.Click the 'Try it out' button.
    2.Enter the authentication token you obtained after verifying the OTP into the 'Authorization' field.
    Example: Token 'your_token' followed by a space(Token 2a16f6b6cfa1f84b647bba8ea45b3ab11a7b3b93).
    3. Click the 'Execute' button to retrieve the response.""",
    manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token", type=openapi.TYPE_STRING),
    ]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Delete User.

    Delete the authenticated user's account.

    :param request: The request object.
    :return: A Response indicating the success of the deletion or an error response.
    """
    user = request.user
    try:
        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': 'An error occurred while deleting the user.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
