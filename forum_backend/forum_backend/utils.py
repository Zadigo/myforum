from django.utils.crypto import get_random_string


def create_id(prefix, length=10):
    """Creates a unique ID string"""
    return f'{prefix}_{get_random_string(length=length)}'
