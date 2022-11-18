class StatusCodeError(Exception):
    """API возвращает код, отличный от 200"""
    def __init__(self, text):
        self.txt = text