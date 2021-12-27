from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from common.services import get_username
from employer.models import Entity
from employer.serializers import EmployerSerializer
from common.serializers import UserSerializer


# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def employer_list(request):
    if request.method == 'GET':
        employers = Entity.objects.all()
        serializer = EmployerSerializer(employers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_data = {
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'email': request.data['email'].lower(),
            'password': make_password(request.data['password']),
            'username': get_username(request.data['email'].lower())
        }
        employer_data = {
            'age': request.data['age'],
            'gender': request.data['gender'],
            'phone': request.data['phone'],
        }

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            employer_serializer = EmployerSerializer(data=employer_data)
            if employer_serializer.is_valid():
                employer_serializer.save(user_id=user.id)
                return Response(employer_serializer.data, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response(employer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
