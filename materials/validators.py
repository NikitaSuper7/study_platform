from rest_framework.serializers import ValidationError


class VideosValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """Проверяет ссылки на материалы"""
        tmp_value = dict(value).get(self.field)
        if tmp_value and len(tmp_value.split(sep=" ")) > 1:
            raise ValidationError("Здесь может быть только одна ссылка")
        if tmp_value and "youtube.com" not in tmp_value:
            raise ValidationError(
                "Можно прикрепить только ссылки на youtube материалы."
            )


class HasLinkValidator:
    """Проверяет наличие ссылки в полях"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if tmp_value and "@" in tmp_value:
            raise ValidationError("Вы не можете прикреплять здесь ссылку")
