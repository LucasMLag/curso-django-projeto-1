from rest_framework import serializers
from tag.models import Tag
from recipes.models import Recipe
from authors.validators import AuthorRecipeValidator


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps', 'cover', 'public', 'preparation', 'category',
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
        # <!> This code block is for the PATCH method, so fields aren't empty and don't cause errors on validations
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings
        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time
        # <!>

        super_validate = super().validate(attrs)

        AuthorRecipeValidator(data=attrs, ErrorClass=serializers.ValidationError)

        return super_validate

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
