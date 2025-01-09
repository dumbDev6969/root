class AppException(Exception):
    """Custom exception class for application errors"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class DatabaseException(Exception):
    """Custom exception class for database errors"""
    def __init__(self, message: str):
        self.status_code = 500
        self.message = f"Database error: {message}"
        super().__init__(self.message)

class ValidationException(Exception):
    """Custom exception class for validation errors"""
    def __init__(self, message: str):
        self.status_code = 400
        self.message = f"Validation error: {message}"
        super().__init__(self.message)
