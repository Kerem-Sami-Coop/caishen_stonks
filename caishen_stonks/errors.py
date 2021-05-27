class InvalidInputError(Exception):
    """Raised when the input value does not match expected set"""
    pass


class MissingEnvVarError(Exception):
    """Raised when there is a missing enviroment variable"""
    pass
