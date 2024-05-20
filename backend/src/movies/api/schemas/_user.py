import pydantic


class BaseUser(pydantic.BaseModel):
    model_config = {"from_attributes": True}

    email: str
    display_name: str


class GetUserResponse(BaseUser):
    model_config = {"from_attributes": True}


class CreateUserRequest(BaseUser):
    model_config = {"from_attributes": False}

    password: str
