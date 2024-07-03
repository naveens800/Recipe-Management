from rest_framework import generics, filters, status
from django.contrib.auth.models import User
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly


@api_view(["POST"])
@permission_classes([AllowAny])
def register_new_user(request):
    """
    This view function is used to register new users.
    """
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
