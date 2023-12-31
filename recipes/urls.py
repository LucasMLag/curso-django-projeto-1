from django.urls import path

from . import views
from rest_framework.routers import SimpleRouter

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    views.RecipeAPIv2ViewSet,
    basename='recipes-api'
    # with the basename, these are the view names:
    # recipes:recipes-api-list
    # recipes:recipes-api-detail pk
)


# This could be used if we were only using the router urls
# urlpatterns = recipe_api_v2_router.urls

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name="home"),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name="search"),
    path('recipes/tags/<slug:slug>/', views.RecipeListViewTag.as_view(), name="tag"),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name="category"),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name="recipe"),
    path('recipes/api/v1/', views.RecipeListViewHomeApi.as_view(), name="recipes_api_v1"),
    path('recipes/api/v1/<int:pk>/', views.RecipeDetailApi.as_view(), name="recipes_api_v1_detail"),

    # <!> This code was replaced by the recipe_api_v2_router
    # path('recipes/api/v2/', views.RecipeAPIv2ViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create',
    # }), name="recipes_api_v2"),
    # path('recipes/api/v2/<int:pk>/', views.RecipeAPIv2ViewSet.as_view({
    #     'get': 'retrieve',
    #     'patch': 'partial_update',
    #     'delete': 'destroy',
    # }), name="recipes_api_v2_detail"),
    # <!>

    path('recipes/api/v2/tag/<int:pk>/', views.tag_api_detail, name="recipes_api_v2_tag"),
]

urlpatterns += recipe_api_v2_router.urls
