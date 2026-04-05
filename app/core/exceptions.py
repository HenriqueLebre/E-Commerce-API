class AppException(Exception):
    """Base exception"""
    def __init__(self, detail: str):
        self.detail = detail

class NotFoundException(AppException):
    """404 — Not Found"""
    pass

class BadRequestException(AppException):
    """400 — Bad Request"""
    pass

class ForbiddenException(AppException):
    """403 — Forbidden"""
    pass

class ConflictException(AppException):
    """409 — Conflict"""
    pass