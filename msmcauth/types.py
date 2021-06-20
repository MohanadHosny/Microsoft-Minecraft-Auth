from requests import Response
from typing import NamedTuple

class PreAuthResponse(NamedTuple):
    response: Response
    url_post: str
    ppft: str

class UserLoginResponse(NamedTuple):
    refresh_token: str
    access_token: str
    expires_in: int
    logged_in: bool = False

class XblAuthenticateResponse(NamedTuple):
    user_hash: str
    token: str

class XSTSAuthenticateResponse(NamedTuple):
    user_hash: str
    token: str

class UserProfile(NamedTuple):
    username: str
    uuid: str

class UserProfileInformation(NamedTuple):
    access_token: str
    username: str
    uuid: str