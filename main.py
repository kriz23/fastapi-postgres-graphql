import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

import models
from db_conf import db_session
from schemas import PostSchema, PostModel

db = db_session.session_factory()
app = FastAPI()


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostModel)
    post_by_id = graphene.Field(PostModel, post_id=graphene.Int(required=True))

    @staticmethod
    def resolve_all_posts(self, info):
        query = PostModel.get_query(info)
        return query.all()

    @staticmethod
    def resolve_post_by_id(self, info, post_id):
        return db.query(models.Post).filter(models.Post.id == post_id).first()


class CreateNewPost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=False)
        content = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, title, author, content):
        post = PostSchema(title=title, author=author, content=content)
        db_post = models.Post(title=post.title, author=post.author, content=post.content)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        ok = True
        return CreateNewPost(ok=ok)


class PostMutations(graphene.ObjectType):
    create_new_post = CreateNewPost.Field()


app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(mutation=PostMutations, query=Query)))