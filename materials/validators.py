from rest_framework.serializers import ValidationError


def validate_urls(value):
    if 'youtube.com' not in value:
        raise ValidationError("Доступен только youtube.com")