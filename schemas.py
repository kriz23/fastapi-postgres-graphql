from graphene_sqlalchemy import SQLAlchemyObjectType
from pydantic import BaseModel

from models import Post


class PostSchema(BaseModel):
    title: str
    author: str
    content: str


class PostModel(SQLAlchemyObjectType):
    class Meta:
        model = Post
