class WrappedException(Exception):
    """A base exception class for wrapping other exceptions with additional context."""
    def __init__(self, original_exception: Exception = None, exception_location: str = None, entry = None):
        self.original_exception = original_exception
        self.exception_location = exception_location or self.__class__.__name__
        self.entry = entry
        super().__init__(str(original_exception) if original_exception else self.exception_location)