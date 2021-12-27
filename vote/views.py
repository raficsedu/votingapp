from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from common.services import get_user_by_token, get_start_of_the_day, get_end_of_the_day
from .models import Entity
from vote.serializers import VoteSerializer
from .services import check_duplicate_vote
from django.db.models import Count
import datetime


# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employer_vote(request):
    # Get user from Token
    token = request.headers['Authorization'].split(' ')[1]
    user = get_user_by_token(token)

    if request.method == 'GET':
        votes = Entity.objects.filter(employer=user.employer)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            # Check for duplicate vote
            is_duplicate = check_duplicate_vote(user.employer.id, request.data['restaurant'])
            if is_duplicate:
                return Response({'message': 'Duplicate vote'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(employer_id=user.employer.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_result(request):
    # Target date, Today if empty
    date = datetime.datetime.strptime(request.data['date'], '%Y-%m-%d') if 'date' in request.data and request.data[
        'date'] else timezone.now().today()

    # Check winner for the target date
    winner_target = Entity.objects.filter(
        created_at__range=(get_start_of_the_day(date), get_end_of_the_day(date))).values('restaurant_id',
                                                                                         'restaurant__name').annotate(
        votes=Count('restaurant_id')).order_by('-votes')[:2]
    winner = winner_target[0] if len(winner_target) else []

    # Check previous 1 day winner
    date = date - datetime.timedelta(days=1)
    winner_past_1 = Entity.objects.filter(
        created_at__range=(get_start_of_the_day(date), get_end_of_the_day(date))).values('restaurant_id',
                                                                                         'restaurant__name').annotate(
        votes=Count('restaurant_id')).order_by('-votes')[:1]

    # Check target winner is winner for last date
    if len(winner_past_1) and len(winner):
        if winner_past_1[0]['restaurant_id'] == winner['restaurant_id']:
            # Check previous 2 day winner
            date = date - datetime.timedelta(days=1)
            winner_past_2 = Entity.objects.filter(
                created_at__range=(get_start_of_the_day(date), get_end_of_the_day(date))).values('restaurant_id',
                                                                                                 'restaurant__name').annotate(
                votes=Count('restaurant_id')).order_by('-votes')[:1]

            # Check target winner is also winner for last 2 consecutive days
            if len(winner_past_2):
                if winner_past_2[0]['restaurant_id'] == winner['restaurant_id']:
                    winner = winner_target[1]

    return Response(winner, status=status.HTTP_200_OK)
