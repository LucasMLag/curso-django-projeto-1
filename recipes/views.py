from typing import Any
from django.http.response import Http404, HttpResponse as HttpResponse
from django.db.models import Q
from utils.pagination import make_pagination
from recipes.models import Recipe
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            is_published=True,
        )

        queryset = queryset.select_related('author', 'category')

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        page_obj, pagination_range = make_pagination(
            self.request, context.get('recipes'), PER_PAGE
        )
        context.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
        })

        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )

    # super().render_to_response(context, **response_kwargs)


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context.update({
            'title': f'{context.get('recipes')[0].category.name} - Category | ',
        })

        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        queryset = super().get_queryset()

        queryset = queryset.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        )

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        search_term = self.request.GET.get('q', '')

        context.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}'
        })

        return context


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            is_published=True,
        )

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context.update({
            'is_detail_page': True,
        })

        return context


class RecipeDetailApi(RecipeDetail):
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False
        )
