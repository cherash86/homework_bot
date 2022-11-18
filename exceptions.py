class NotForSending(Exception):
    """Не для пересылки в телеграм."""
    pass


class ProblemDescriptions(Exception):
    """Описания проблемы."""
    pass


class InvalidResponseCode(Exception):
    """Не верный код ответа."""
    pass


class ConnectinError(Exception):
    """Не верный код ответа."""
    pass


class EmptyResponseFromAPI(NotForSending):
    """Пустой ответ от API."""
    pass


class TelegramError(NotForSending):
    """Ошибка телеграма."""
    pass


class StatusCodeError(Exception):
    """API возвращает код, отличный от 200"""
    def __init__(self, text):
        self.txt = text