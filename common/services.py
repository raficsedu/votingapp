import uuid
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import datetime
from django.utils.timezone import make_aware


def get_username(email):
    user_name = email.split("@")[0]

    # Check if username exist
    try:
        User.objects.get(username=user_name)
        user_name = user_name + "_" + uuid.uuid4().hex[:3]
    except User.DoesNotExist:
        user_name = user_name

    return user_name


def get_user_token(user):
    token = Token.objects.filter(user=user)
    if len(token) > 0:
        token = token.first()
    else:
        token = Token.objects.create(user=user)

    return token


def reset_user_token(token):
    user = get_user_by_token(token)
    Token.objects.get(user=user).delete()
    token = get_user_token(user)

    return token


def get_user_by_token(token):
    return Token.objects.get(key=token).user


def get_start_of_the_day(date=datetime.date.today()):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return make_aware(datetime.datetime.combine(date, datetime.time.min))


def get_end_of_the_day(date=datetime.date.today()):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return make_aware(datetime.datetime.combine(date, datetime.time.max))
