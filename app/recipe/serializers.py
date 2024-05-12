from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    "A serializer for Recipe Model"
    class Meta:
        model = Recipe
        fields = '__all__'