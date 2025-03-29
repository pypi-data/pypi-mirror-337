class ValidationError(Exception):
    """Exception raised if validation failed.

    Args:
        Exception (_type_): _description_
    """

    def __init__(self) -> None:
        self.message = "Validation failed."
        super().__init__(self.message)
