from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from common.services import get_username, get_user_by_token, get_start_of_the_day, get_end_of_the_day
from restaurant.models import Entity, Menu
from restaurant.serializers import RestaurantSerializer, MenuSerializer
from common.serializers import UserSerializer
from django.http import JsonResponse
from restaurant.services import get_formatted_menus
import datetime


# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def restaurant_list(request):
    if request.method == 'GET':
        restaurants = Entity.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_data = {
            'first_name': request.data['name'],
            'last_name': 'Admin',
            'email': request.data['email'].lower(),
            'password': make_password(request.data['password']),
            'username': get_username(request.data['email'].lower())
        }
        restaurant_data = {
            'name': request.data['name'],
            'address': request.data['address'],
            'phone': request.data['phone'],
        }

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            restaurant_serializer = RestaurantSerializer(data=restaurant_data)
            if restaurant_serializer.is_valid():
                restaurant_serializer.save(user_id=user.id)
                return Response(restaurant_serializer.data, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def menu_list(request):
    token = request.headers['Authorization'].split(' ')[1]
    user = get_user_by_token(token)
    if request.method == 'GET':
        menus = list(Menu.objects.filter(entity=user.restaurant,
                                         created_at__range=(get_start_of_the_day(), get_end_of_the_day())))
        return JsonResponse({'date': datetime.date.today(), **get_formatted_menus(menus)}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if getattr(user, 'restaurant', None):
            if 'menus' in request.data:
                menu_data = request.data['menus']
                for menu in menu_data:
                    if 'date' in request.data and request.data['date']:
                        menu['created_at'] = request.data['date']
                    serializer = MenuSerializer(data=menu)
                    if serializer.is_valid():
                        serializer.save(entity_id=user.restaurant.id)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse(request.data, status=status.HTTP_201_CREATED)
            else:
                return Response('menu index is missing', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Restaurant not found', status=status.HTTP_404_NOT_FOUND)
