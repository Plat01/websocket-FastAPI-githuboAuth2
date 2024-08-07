from pydantic import BaseModel, Field


class OAuthTokenResponse(BaseModel):
    access_token: str = Field(..., description="The access token issued by the authorization server")
    token_type: str = Field(..., description="The type of token, typically 'bearer'")
    scope: str = Field("", description="The scope of the access token")


class User(BaseModel):
    id: int
    login: str
    token: str
    name: str | None = None
    email: str | None = None
