import pathlib

from django.conf import settings
from django.core.cache import cache
from nltk.tokenize import TweetTokenizer
from rest_framework.exceptions import ValidationError


def moderate_text(text=None, tokens=[]):
    if text is not None:
        instance = TweetTokenizer()
        tokens = instance.tokenize(text)

    if text is None and not tokens:
        return True

    stop_words = cache.get('stop_words', None)

    if stop_words is None:
        file_path = pathlib.Path(settings.MEDIA_ROOT, 'stop_words.txt')
        with open(file_path, mode='r', encoding='utf-8') as f:
            # TODO: Words like b*tch does not get
            # detected by the automated moderator
            stop_words = f.read().splitlines()
            cache.set('stop_words', stop_words, 3600)

    invalid_words = list(map(lambda x: x in stop_words, tokens))

    if any(invalid_words):
        raise ValidationError(detail='Comment contains invdalid words')

    return True


def moderate_text_validator(text):
    moderate_text(text=text)
    text = text.lower().title()
    return text
