from common.services import get_start_of_the_day, get_end_of_the_day
from .models import Entity


def check_duplicate_vote(employer_id, restaurant_id):
    vote = Entity.objects.filter(employer_id=employer_id, restaurant_id=restaurant_id,
                                 created_at__range=(get_start_of_the_day(), get_end_of_the_day()))

    return True if len(vote) else False
