# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class PatentClassError(Error):
    """Raised when the input value is too small"""
    pass

class NoPatentsError(Error):
    """Raised when no patents to scrape"""
    pass