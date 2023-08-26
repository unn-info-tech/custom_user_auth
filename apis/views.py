from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserRegistrationSerializer, UserLoginSerializer, VerifyOTPSerializer

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .tasks import send_otp_email, generate_and_store_otp
from django.core.exceptions import ObjectDoesNotExist
import time
from django.core.cache import cache



# REGISTER
@api_view(['POST'])
def register_user(request):
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
@api_view(['POST'])
def user_login(request):
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
                
                # this one is for celery
                # send_otp_email(user.email, generated_otp) 
                print('This is otp for test:', generated_test_otp)

                # Store the values in the session for later validation
                request.session['generated_test_otp'] = generated_test_otp
                request.session['user_id'] = user.id
                
                return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Verify OTP and issue token
@api_view(['POST'])
def verify_otp(request):
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
        
        cached_otp = cached_data.get('otp')
        cached_timestamp = cached_data.get('timestamp')
        
        # Check if the provided OTP matches the cached OTP
        if input_otp == cached_otp:
            # Check if OTP has expired
            current_timestamp = int(time.time())
            expiration_time = 15  # OTP expires in 5 minutes (300 seconds)
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





#UPDATE
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserRegistrationSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        hashed_password = make_password(serializer.validated_data['password'])
        user = serializer.save(password=hashed_password)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#PROFILE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        user = request.user
        profile_data = {
            'username': user.username,
            'email': user.email,
        }
        return Response(profile_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# LOGOUT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
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
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    try:
        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': 'An error occurred while deleting the user.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
