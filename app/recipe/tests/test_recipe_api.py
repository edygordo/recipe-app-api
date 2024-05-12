"""
Tests for Recipe API
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    "Create and return a recipe detail url"
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(user, **params):
    " Create and return a sample recipe "
    defaults = {
        "user": user,
        "title": "Sample recipe title",
        "time_minutes": 22,
        "price": Decimal("5.25"),
        "description": "Sample Description",
        "link": "http://example.com/recipe.pdf",
    }
    recipe = Recipe.objects.create(**defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    "Test unauthorized API request"

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        "an unauthenticated user can't get list of recipes!"
        res = self.client.get(path=RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    "Test authorized request"

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com", name="Test User", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipe(self):
        "Test retrieving list of recipe"
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by(
            "-id"
        )  # Decending order of ID retrieving
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        "Test list of recipes is limited to authenticated user"
        other_user = get_user_model().objects.create_user(
            email="otheruser@example.com", name="Other User", password="testpass123" #noqa
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        # Client is authenticated with self.user
        res = self.client.get(path=RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        "Test detail view of a recipe"
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe_id=recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
