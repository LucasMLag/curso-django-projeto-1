from rest_framework import serializers
from recipes.models import Category
from django.contrib.auth.models import User
from tag.models import Tag
from recipes.models import Recipe
from collections import defaultdict

# v1 serializers.Serializer:
# class TagSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=255)
#     slug = serializers.SlugField()


# v2 serializers.ModelSerializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


# v1 serializers.Serializer
# class RecipeSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=65)
#     description = serializers.CharField(max_length=165)
#     public = serializers.BooleanField(source='is_published')
#     preparation = serializers.SerializerMethodField(method_name='get_preparation')
#     # category = serializers.PrimaryKeyRelatedField(
#     #     queryset=Category.objects.all()
#     # )
#     category = serializers.StringRelatedField()
#     author = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all()
#     )
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=Tag.objects.all(),
#         many=True
#     )
#     tag_objects = TagSerializer(
#         many=True,
#         source='tags'
#     )
#     tag_links = serializers.HyperlinkedRelatedField(
#         many=True,
#         source='tags',
#         queryset=Tag.objects.all(),
#         view_name='recipes:recipes_api_v2_tag',
#     )
#
#     def get_preparation(self, recipe):
#         return f'{recipe.preparation_time} {recipe.preparation_time_unit}'


# v2 serializers.ModelSerializer
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'public', 'preparation', 'category',
            'author', 'tags', 'tag_objects', 'tag_links',
        ]
    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
    )
    preparation = serializers.SerializerMethodField(
        method_name='get_preparation',
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True,
        source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    # validate for multiple fields
    def validate(self, attrs):
        super_validate = super().validate(attrs)

        title = attrs.get('title')
        description = attrs.get('description')

        if title == description:
            raise serializers.ValidationError(
                {
                    "title": [
                        "Title can't be equal to description.",
                        # "It's possible to put multiple erros!",
                    ],
                    "description": ["Description can't be equal to title.",],
                }
            )

        return super_validate

    # validate_field for one fields
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Must have at least 5 chars.')
        return value
