from rest_framework import generics, filters
from django.contrib.auth.models import User
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly


class RegisterView(generics.CreateAPIView):
    "This view class is used to register new users."
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class RecipeListCreateView(generics.ListCreateAPIView):
    "This view class is used to create and list recipes."
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "ingredients"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RecipeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    "This view class is used to retrieve, update, and delete recipes."
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
