import pydantic


class BaseUser(pydantic.BaseModel):
    model_config = {"from_attributes": True}

    username: str


class User(BaseUser):
    model_config = {"from_attributes": True}

    id: int


class CreateUser(BaseUser):
    model_config = {"from_attributes": False}

    password: str
