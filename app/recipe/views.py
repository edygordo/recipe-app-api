"Views for Recipe API"

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    "View for managing recipe APIs. "
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by(
            "-id"
        )  # This self.request will be None if user not authenticated

    def get_serializer_class(self):
        "Return proper serializer class for requests"
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        "Override creation of object in the model"
        serializer.save(user=self.request.user)
