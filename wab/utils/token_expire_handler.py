from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token


def expires_in(token):
    # this return left time
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time


def is_token_expired(token):
    # token checker if token expired or not
    return expires_in(token) < timedelta(seconds=0)



def token_expire_handler(token):
    # if token is expired new token will be established
    # If token is expired then it will be removed
    # and new one with different key will be created
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token
