from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_orm = True
        from_attributes = True


class Pagginate(BaseSchema):
    current_page: int = 1
    pages: int = 1
