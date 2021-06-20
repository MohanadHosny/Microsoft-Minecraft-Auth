class MsMcAuthException(Exception):
    def __init__(self, message):
        super().__init__(message)

class XblAuthenticationFailed(MsMcAuthException):
    """Xbl Authentication failed (status code is not 200)."""
    pass

class XstsAuthenticationFailed(MsMcAuthException):
    """Xsts Authentication failed."""
    pass

class LoginWithXboxFailed(MsMcAuthException):
    """LoginWithXbox Authentication failed."""
    pass

class NoXboxAccount(MsMcAuthException):
    """This account doesn't have an Xbox account."""
    pass

class ChildAccount(MsMcAuthException):
    """The account is a child account (under 18)."""
    pass

class TwoFactorAccount(MsMcAuthException):
    """2FA is enabled but not supported yet."""
    pass

class InvalidCredentials(MsMcAuthException):
    """Provided credentials was invalid."""
    pass

class NotPremium(MsMcAuthException):
    """Account is not premium."""
    pass