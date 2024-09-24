class FyleError(Exception):
    """Custom exception class for Fyle errors."""

    def __init__(self, status_code: int = 400, message: str = "An error occurred") -> None:
        """Initializes the FyleError with a status code and message.

        Args:
            status_code (int): The HTTP status code for the error. Defaults to 400.
            message (str): A message describing the error. Defaults to "An error occurred".
        """
        super().__init__(message)  # Call the base class constructor
        self.message = message
        self.status_code = status_code

    def to_dict(self) -> dict:
        """Converts the error to a dictionary representation.

        Returns:
            dict: A dictionary containing the error message and status code.
        """
        return {
            'message': self.message,
            'status_code': self.status_code
        }

    def __str__(self) -> str:
        """Returns a string representation of the error."""
        return f"FyleError(status_code={self.status_code}, message='{self.message}')"
