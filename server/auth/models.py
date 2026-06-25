from pydantic  import BaseModel


class SignupRequest(BaseModel):
    username: str
    role: str
    password: str 