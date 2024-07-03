from django.urls import path
from .views import RecipeRetrieveUpdateDestroyView, RecipeListCreateView, RegisterView

urlpatterns = [
    path("recipes/", RecipeListCreateView.as_view(), name="recipe-list-create"),
    path(
        "recipes/<int:pk>/",
        RecipeRetrieveUpdateDestroyView.as_view(),
        name="recipe-detail",
    ),
    path("register/", RegisterView.as_view(), name="register"),
]
