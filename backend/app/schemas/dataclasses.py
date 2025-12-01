from dataclasses import dataclass


@dataclass
class AuthTokens:
    access_token: str | None
    refresh_token: str | None
    is_access_token_update: bool
    is_refresh_token_update: bool
