# Microsoft-Minecraft-Auth
Microsoft-Minecraft-Auth is a simple xbox minecraft auth

# How to install
```
pip install msmcauth
```

# Example of usage
```py


import msmcauth

resp = msmcauth.login("email", "password")

"""
You can get the access token or username or user id(Uuid)
resp.access_token
resp.username
resp.id
"""

print(resp) # You handle the response
```

# Changelog
Added
  - errors
  - new types
  - comments
