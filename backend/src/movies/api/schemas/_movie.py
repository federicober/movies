import pydantic


class Movie(pydantic.BaseModel):
    title: str
    image_url: str
