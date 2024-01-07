from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from tag.models import Tag
from ..serializers import TagSerializer

from ..models import Recipe
from ..serializers import RecipeSerializer


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(
            data=request.data,
        )
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


@api_view()
def recipe_api_detail(request, pk):

    # <option 1> Looks for a recipe, if not found returns response {"detail": "not found"} and status code 404

    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serializer = RecipeSerializer(
        instance=recipe,
        context={'request': request},
    )
    return Response(serializer.data)

    # <!>

    # <option 2> looks for a recipe, if not found allows you to set response, and status code

    # recipe = Recipe.objects.get_published().filter(pk=pk).first()

    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe)
    #     return Response(serializer.data)
    # else:
    #     return Response(status=status.HTTP_418_IM_A_TEAPOT)

    # <!>


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        context={'request': request},
    )
    return Response(serializer.data)
