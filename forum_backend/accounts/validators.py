from django.core.exceptions import ValidationError


def ban_days_validator(value):
    """Checks that the number of days for which
    a user is banned is between 3 and 15 days"""
    if value == 0:
        return

    
    if value > 3 and value <= 15:
        return

    raise ValidationError('Ban days should be between 3 and 15 days')
