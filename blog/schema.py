import graphene
from graphene_django import DjangoObjectType
from .models import Post, PostCategory, Like
from graphql import GraphQLError
from users.schema import AuthorType
from django.db.models import Q


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class PostCatType(DjangoObjectType):
    class Meta:
        model = PostCategory


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class Query(graphene.ObjectType):
    posts = graphene.List(PostType, search=graphene.String())

    post = graphene.Field(PostType,
                          id=graphene.Int(),
                          )
    postCats = graphene.List(PostCatType)
    likes = graphene.List(LikeType)

    def resolve_posts(self, info, search=None):
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(author__username__icontains=search) |
                Q(category__cat_title__icontains=search) |
                Q(category__cat_desc__icontains=search)

            )
            return Post.objects.filter(filter)
        return Post.objects.all()

    def resolve_postCats(self, info, **kwargs):

        return PostCategory.objects.all()

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Post.objects.get(pk=id)

        return None

    def resolve_likes(self, info):
        return Like.objects.all()


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String()
        content = graphene.String()
        thumb = graphene.String()
        category = graphene.String()

    def mutate(self, info, **kwargs):
        author = info.context.user
        if author.is_anonymous:
            raise Exception("Login required")
        post = Post(**kwargs, author=author)
        post.save()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()
        thumb = graphene.String()

    def mutate(self, info, post_id, content, thumb, title):
        author = info.context.user
        post = Post.objects.get(id=post_id)
        if post.author != author:
            raise Exception("You are not permitted to update this post")
        post.content = content
        post.thumb = thumb
        post.title = title
        post.save()

        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    post_id = graphene.Int()

    class Arguments:
        post_id = graphene.Int(required=True)

    def mutate(self, info, post_id):
        author = info.context.user
        post = Post.objects.get(id=post_id)

        if post.author != author:
            raise Exception("You are not allowed to delete this post")

        post.delete()
        return DeletePost(post=post)


class CreateLike(graphene.Mutation):
    author = graphene.Field(AuthorType)
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.Int(required=True)

    def mutate(self, info, post_id):
        author = info.context.author

        if author.is_anonymous:
            raise Exception("Login to like this post")

        post = Post.objects.get(id=post_id)

        if not post:
            raise Exception("No post with the provided query")

        Like.objects.create(
            author=author,
            post=post
        )

        return CreateLike(author=author, post=post)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    like_post = CreateLike.Field()
