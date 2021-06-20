from requests import Session
from .types import UserLoginResponse, XblAuthenticateResponse, XSTSAuthenticateResponse, UserProfile
from .consts import XBL, XSTS, LOGIN_WITH_XBOX, OWNERSHIP, PROFILE, USER_AGENT
from .errors import XblAuthenticationFailed, XstsAuthenticationFailed, ChildAccount, NoXboxAccount, LoginWithXboxFailed

class Microsoft:
    def __init__(self, client: Session = None) -> None:
        self.client = client if client is not None else Session()
        
    def xbl_authenticate(self, login_resp: UserLoginResponse) -> XblAuthenticateResponse:
        """
        Xbl Authenticate.

        Parameters:
            login_resp (UserLoginResponse): :class:`UserLoginResponse` object

        :return: :class:`XblAuthenticateResponse` object
        """

        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "x-xbl-contract-version": "0"
        }

        payload = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": login_resp.access_token,
            }
        }

        resp = self.client.post(XBL, json=payload, headers=headers)
        
        if resp.status_code != 200:
            raise XblAuthenticationFailed("Xbl Authentication failed (status code is not 200).")

        data = resp.json()

        return XblAuthenticateResponse(
            token=data["Token"],
            user_hash=data["DisplayClaims"]["xui"][0]["uhs"]
        )

    def xsts_authenticate(self, xbl_resp: XblAuthenticateResponse) -> XSTSAuthenticateResponse:
        """
        Xsts Authenticate.

        Parameters:
            xbl_resp (XblAuthenticateResponse): Xbl response.

        :return: :class:`XSTSAuthenticateResponse`
        """

        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "x-xbl-contract-version": "1"
        }

        payload = {
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT",
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [
                    xbl_resp.token
                ]
            }
        }

        resp = self.client.post(XSTS, json=payload, headers=headers)

        if resp.status_code != 200:
            if resp.status_code == 401:
                json = resp.json()
                if json["XErr"] == "2148916233":
                    raise NoXboxAccount("This account doesn't have an Xbox account.")
                elif json["XErr"] == "2148916238":
                    raise ChildAccount("The account is a child account (under 18).")
                else:
                    raise Exception(f"Unknown Xsts Error code: {json['XErr']}")
            else:
                raise XstsAuthenticationFailed("Xsts Authentication failed.")

        data = resp.json()

        return XSTSAuthenticateResponse(
            token=data["Token"],
            user_hash=data["DisplayClaims"]["xui"][0]["uhs"]
        )

    def login_with_xbox(self, token: str, user_hash: str) -> str:
        """
        Login with xbox.

        Parameters:
            user_hash (str): XSTS response token.
            token (str): XSTS response user_hash.

        :return: Access token
        """

        headers = {
            "Accept": "application/json",
            "User-Agent": USER_AGENT
        }

        payload = {"identityToken": f"XBL3.0 x={user_hash};{token}"}
        
        resp = self.client.post(LOGIN_WITH_XBOX, json=payload, headers=headers)
        
        if "access_token" not in resp.text:
            raise LoginWithXboxFailed("LoginWithXbox Authentication failed.")
        
        return resp.json()["access_token"]

    def user_hash_game(self, access_token: str) -> bool:
        """
        Checks if user has mc game.

        Parameters:
            access_token (str): Access token.
        
        :return: Boolean
        """

        headers = {
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {access_token}"
        }

        resp = self.client.get(OWNERSHIP, headers=headers)
                
        return len(resp.json()["items"]) > 0

    def get_user_profile(self, access_token: str) -> UserProfile:
        """
        Check user mc profile information.

        Parameters:
            access_token (str): Access token.

        :return: :class:`UserProfile`
        """

        headers = {
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {access_token}"
        }

        resp = self.client.get(PROFILE, headers=headers).json()
                
        return UserProfile(
            username=resp["name"],
            uuid=resp["id"]
        )
