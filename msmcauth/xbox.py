import requests
from .types import PreAuthResponse, UserLoginResponse
from .consts import USER_AGENT, AUTHORIZE
from .errors import InvalidCredentials, TwoFactorAccount
from re import search

class XboxLive:
    def __init__(self, client: requests.Session = None) -> None:
        self.client = client if client is not None else requests.Session()

    def pre_auth(self) -> PreAuthResponse:
        """
        Live pre auth.
        
        :return: :class:`PreAuthResponse`
        """
        resp = self.client.get(AUTHORIZE, headers={"User-Agent": USER_AGENT}, allow_redirects=True)

        ppft = search(r"value=\"(.*?)\"", search(r"sFTTag:'(.*?)'", resp.text).group(1)).group(1)
        urlPost = search(r"urlPost:'(.+?(?=\'))", resp.text).group(1)

        if urlPost is None or ppft is None:
            raise Exception("Failed to extract PPFT or urlPost")

        return PreAuthResponse(
            response=resp,
            ppft=ppft,
            url_post=urlPost
        )

    def user_login(self, email: str, password: str, preauth: PreAuthResponse) -> UserLoginResponse:
        """
        Checks user credentials.

        Parameters:
            email (str): AUTHORIZE email
            password (str): AUTHORIZE password
            preauth (PreAuthResponse): class:`PreAuthResponse` object

        :return: class:`UserLoginResponse` object
        """

        postData = f"login={self.encode(email)}&loginfmt={self.encode(email)}&passwd={self.encode(password)}&PPFT={preauth.ppft}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT
        }

        resp = self.client.post(url=preauth.url_post, data=postData, cookies=preauth.response.cookies, headers=headers, allow_redirects=True)

        if "access_token" not in resp.url and resp.url == preauth.url_post:
            if "Sign in to" in resp.text:
                raise InvalidCredentials("Provided credentials was invalid.")
            elif "Help us protect your account" in resp.text:
                raise TwoFactorAccount("2FA is enabled but not supported yet.")
            else:
                raise Exception(f"Something went wrong. Status Code: {resp.status_code}")

        data = resp.url.split("#")[1].split("&")

        return UserLoginResponse(
            refresh_token=data[4].split("=")[1],
            access_token=data[0].split("=")[1],
            expires_in=int(data[2].split("=")[1]),
            logged_in=True
        )

    def encode(self, data: str) -> str:
        """
        Encodes data.
        
        Parameters:
            data (str): Data to encode

        :return: Encoded data
        """

        return requests.utils.quote(data)

    