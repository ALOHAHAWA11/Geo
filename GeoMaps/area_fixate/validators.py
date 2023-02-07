import re

from django.core.exceptions import ValidationError


def check_cadastral(number):
    if not re.match(r'^\d{2}:\d{2}:\d{1,7}:\d*$', number):
        raise ValidationError('Недопустимый формат кадастрового номера!')