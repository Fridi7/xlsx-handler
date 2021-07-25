from hashlib import sha256

from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class CustomTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request=None):
        auth_components = request.META.get('HTTP_AUTHORIZATION', '').split(' ')
        if len(auth_components) == 2 and auth_components[0] == 'Token':
            token = auth_components[1]

            user = User.objects.get_or_create()  # user only for auth

            if token == token_sign():
                return user, token

        raise AuthenticationFailed()


def token_sign() -> str:
    """
    sha256 hash current date
    """
    date_now = str(now().date())

    sha = sha256()
    sha.update(bytes(date_now, encoding="utf-8"))

    return sha.hexdigest()


def has_duplicates(values: list) -> bool:
    return len(values) != len(set(values))


def get_rep_count(list1: list, list2: list) -> set:
    from collections import Counter

    value_counter1 = dict(Counter(list1))
    value_counter2 = dict(Counter(list2))

    return set(value_counter1.items()) ^ set(value_counter2.items())


def get_pretty_list_from_string(string: str) -> list:
    """
    example:
     in: ' 4, 3124124, -1, '
     out: ['4', '3124124', '-1']
     """
    return string.strip(', ').split(', ')
