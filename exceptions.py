class StatusCodeError(Exception):
    """API возвращает код, отличный от 200"""
    pass

class NotForSend(Exception):
    """Исключение не для пересылки в telegram."""
    pass


class TelegramError(Exception):
    """Ошибка телеграма."""
    pass


class WrongResponseCode(Exception):
    """Неверный ответ API."""
    pass