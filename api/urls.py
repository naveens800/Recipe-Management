from django.urls import path
from .views import RecipeRetrieveUpdateDestroyView, RecipeListCreateView, register_new_user

urlpatterns = [
    path("recipes/", RecipeListCreateView.as_view(), name="recipe-list-create"),
    path(
        "recipes/<int:pk>/",
        RecipeRetrieveUpdateDestroyView.as_view(),
        name="recipe-detail",
    ),
    path("register/", register_new_user, name="register"),
]
