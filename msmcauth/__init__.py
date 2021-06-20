from .xbox import XboxLive
from requests import Session
from .microsoft import Microsoft
from .types import PreAuthResponse, UserProfile, UserLoginResponse, XSTSAuthenticateResponse, XblAuthenticateResponse, UserProfileInformation
from .errors import InvalidCredentials, TwoFactorAccount, XblAuthenticationFailed, XstsAuthenticationFailed, ChildAccount, NoXboxAccount, LoginWithXboxFailed, NotPremium

def login(email: str, password: str, client = None) ->  UserProfileInformation:
    """
    Login 
    Parameters:
        email (str): Email for authorize.
        password (str): password for authorize.
        client (requests.Session): Requests session (default) :class:`requests.Session`.

    :return: (UserProfileInformation) if auth was successful.
    """
    
    client = client if client is not None else Session()
    
    xbx = XboxLive(client)
    mic = Microsoft(client)

    login = xbx.user_login(email, password, xbx.pre_auth())

    xbl = mic.xbl_authenticate(login)
    xsts = mic.xsts_authenticate(xbl)
    
    access_token = mic.login_with_xbox(xsts.token, xsts.user_hash)
    has_game = mic.user_hash_game(access_token)
    
    if has_game:
        profile = mic.get_user_profile(access_token)
        data = UserProfileInformation(
            access_token=access_token,
            username=profile.username,
            uuid=profile.uuid
        )

        return data

    raise NotPremium("Account is not premium.")
