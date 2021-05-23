from msmcauth.microsoft import Microsoft
from msmcauth.xbox import XboxLive
from msmcauth.consts import *
from msmcauth.types import *

from requests import Session

def login(email: str, password: str):
    try:
        client = Session()
        
        xbx = XboxLive(client)
        mic = Microsoft(client)

        login = xbx.user_login(email, password, xbx.pre_auth())

        xbl = mic.xbl_authenticate(login)
        xsts = mic.xsts_authenticate(xbl)
        
        access_token = mic.login_with_xbox(xsts.token, xsts.user_hash)
        hasGame = mic.user_hash_game(access_token)
        
        if hasGame:
            profile = mic.get_user_profile(access_token)
            data = {
                "access_token": access_token,
                "username": profile.username,
                "uuid": profile.uuid
            }

            return data
        else:
            return "Not a premium account"
    except Exception as ex:
        return f"Microsoft authenticate failed: {str(ex)}"
