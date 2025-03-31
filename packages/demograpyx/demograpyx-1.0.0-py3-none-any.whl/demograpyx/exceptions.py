__all__ = ("ApiKeyWarning", "HTTPError")

class ApiKeyWarning(Warning):
    """Warning used when API key is not present
    """
    pass

class HTTPError(Exception):
    """HTTP exception class
    """
    def __init__(self, message: str, code: int) -> None:
        """
        Args:
            message (str): The message displayed
            code (int): The associated HTTP error code
        """
        super().__init__(message)
        self.code = code