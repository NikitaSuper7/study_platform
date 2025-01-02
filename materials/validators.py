from rest_framework.serializers import ValidationError


class VideosValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """Проверяет ссылки на материалы"""
        tmp_value = dict(value).get(self.field)
        tmp_value_list = tmp_value.split(sep=" ")
        if len(tmp_value_list) > 1:
            raise ValidationError("Здесь может быть только одна ссылка")
        if "youtube.com" not in tmp_value:
            raise ValidationError(
                "Можно прикрепить только ссылки на youtube материалы."
            )


class HasLinkValidator:
    """Проверяет наличие ссылки в полях"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if "@" in tmp_value:
            raise ValidationError("Вы не можете прикреплять здесь ссылку")
