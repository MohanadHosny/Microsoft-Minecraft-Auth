from requests import Session
from .types import *
from .consts import *

class Microsoft:
    def __init__(self, client: Session = None) -> None:
        self.client = client if client is not None else Session()
        
    def xbl_authenticate(self, login_resp: UserLoginResponse) -> XblAuthenticateResponse:
        headers = {
            "User-Agent": userAgent,
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

        resp = self.client.post(Xbl, json=payload, headers=headers)
        
        if resp.status_code != 200:
            raise Exception("XBL Authentication failed")

        data = resp.json()

        return XblAuthenticateResponse(
            token=data["Token"],
            user_hash=data["DisplayClaims"]["xui"][0]["uhs"]
        )

    def xsts_authenticate(self, xbl_resp: XblAuthenticateResponse) -> XSTSAuthenticateResponse:
        headers = {
            "User-Agent": userAgent,
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

        resp = self.client.post(Xsts, json=payload, headers=headers)

        if resp.status_code != 200:
            if resp.status_code == 401:
                json = resp.json()
                if json["XErr"] == "2148916233":
                    raise Exception("This account doesn't have an Xbox account")
                elif json["XErr"] == "2148916238":
                    raise Exception("The account is a child (under 18)")
                else:
                    raise Exception(f"Unknown XSTS error code: {json['XErr']}")
            else:
                raise Exception("XSTS Authentication failed")

        data = resp.json()

        return XSTSAuthenticateResponse(
            token=data["Token"],
            user_hash=data["DisplayClaims"]["xui"][0]["uhs"]
        )

    def login_with_xbox(self, token: str, user_hash: str) -> str:
        headers = {
            "Accept": "application/json",
            "User-Agent": userAgent
        }

        payload = {"identityToken": f"XBL3.0 x={user_hash};{token}"}
        
        resp = self.client.post(login_with_xbox, json=payload, headers=headers)
        
        if "access_token" not in resp.text:
            raise Exception("LoginWithXbox Authentication failed")
        
        return resp.json()["access_token"]

    def user_hash_game(self, access_token: str) -> bool:
        headers = {
            "Accept": "application/json",
            "User-Agent": userAgent,
            "Authorization": f"Bearer {access_token}"
        }

        resp = self.client.get(ownership, headers=headers)
                
        return len(resp.json()["items"]) > 0

    def get_user_profile(self, access_token: str) -> UserProfile:
        headers = {
            "Accept": "application/json",
            "User-Agent": userAgent,
            "Authorization": f"Bearer {access_token}"
        }

        resp = self.client.get(profile, headers=headers).json()
                
        return UserProfile(
            username=resp["name"],
            uuid=resp["id"]
        )
