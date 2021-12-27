from django.contrib.auth import authenticate
from django.shortcuts import HttpResponse, render
from common.serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from common.services import get_user_token, reset_user_token


# Create your views here.
def index(request):
    return render(request, 'common/index.html', {})


@api_view(['POST'])
@permission_classes([AllowAny])
def user_authenticate(request):
    user = authenticate(request, email=request.data['email'], password=request.data['password'])
    if user:
        token = get_user_token(user)
        user_data = UserSerializer(user).data.copy()
        user_data.pop('password')

        # Check user type
        if getattr(user, 'employer', None):
            user_data['employer_id'] = user.employer.id
            user_data['age'] = user.employer.age
            user_data['gender'] = user.employer.gender
            user_data['phone'] = user.employer.phone
        else:
            user_data['restaurant_id'] = user.restaurant.id
            user_data['name'] = user.restaurant.name
            user_data['address'] = user.restaurant.address
            user_data['phone'] = user.restaurant.phone
            user_data.pop('first_name')
            user_data.pop('last_name')

        # Assign Token
        user_data['token'] = token.key
        return Response(user_data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Login Failed'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    token = request.headers['Authorization'].split(' ')[1]
    reset_user_token(token)
    return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
