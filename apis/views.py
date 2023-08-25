from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserRegistrationSerializer, UserLoginSerializer

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from .models import CustomUser

    
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
            # Check user's password
            if user.check_password(password):
                # Authenticate user
                auth_user = authenticate(username=user.email, password=password)
                if auth_user:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

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
