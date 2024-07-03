from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Recipe
import json


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")


class TokenObtainPairViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token_obtain_pair_url = reverse("token_obtain_pair")

    def test_obtain_token_pair(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.token_obtain_pair_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class TokenRefreshViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.refresh_token_url = reverse("token_refresh")

    def test_refresh_token(self):
        refresh_token = RefreshToken.for_user(self.user)
        data = {"refresh": str(refresh_token)}
        response = self.client.post(self.refresh_token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


class RecipeListCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.recipe_list_url = reverse("recipe-list-create")
        self.recipe_data = {
            "title": "Test Recipe",
            "description": "This is a test recipe",
            "ingredients": "Ingredient 1, Ingredient 2",
            "instructions": "Step 1, Step 2",
        }

    def test_create_recipe(self):
        response = self.client.post(
            self.recipe_list_url, self.recipe_data, format="json"
        )
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, "Test Recipe")
        recipe = Recipe.objects.filter(**self.recipe_data).first()
        self.assertEqual(recipe.created_by, self.user)

    def test_list_recipes(self):
        Recipe.objects.create(
            title="Recipe 1",
            ingredients="Ingredient 1",
            instructions="Step 1",
            created_by=self.user,
        )
        Recipe.objects.create(
            title="Recipe 2",
            ingredients="Ingredient 2",
            instructions="Step 2",
            created_by=self.user,
        )
        response = self.client.get(self.recipe_list_url)
        if response.status_code != status.HTTP_200_OK:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class RecipeUpdateDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="This is a test recipe",
            ingredients="Ingredient 1, Ingredient 2",
            instructions="Step 1, Step 2",
            created_by=self.user,
        )
        self.other_recipe = Recipe.objects.create(
            title="Other Recipe",
            description="This is another recipe",
            ingredients="Ingredient 3, Ingredient 4",
            instructions="Step 3, Step 4",
            created_by=self.other_user,
        )

    def test_update_recipe(self):
        url = reverse("recipe-detail", args=[self.recipe.id])
        data = {
            "title": "Updated Recipe",
            "description": "This is an updated recipe",
            "ingredients": "Updated Ingredient 1, Updated Ingredient 2",
            "instructions": "Updated Step 1, Updated Step 2",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "Updated Recipe")
        self.assertEqual(
            self.recipe.ingredients, "Updated Ingredient 1, Updated Ingredient 2"
        )

    def test_delete_recipe(self):
        url = reverse("recipe-detail", args=[self.recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())

    def test_update_other_user_recipe(self):
        url = reverse("recipe-detail", args=[self.other_recipe.id])
        data = {
            "title": "Updated Other Recipe",
            "description": "This is an updated other recipe",
            "ingredients": "Updated Other Ingredient 1, Updated Other Ingredient 2",
            "instructions": "Updated Other Step 1, Updated Other Step 2",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_other_user_recipe(self):
        url = reverse("recipe-detail", args=[self.other_recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Recipe.objects.filter(id=self.other_recipe.id).exists())


class RecipeSearchViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.recipe1 = Recipe.objects.create(
            title="Chicken Curry",
            description="A delicious chicken curry recipe",
            ingredients='["chicken", "onions", "tomatoes", "curry powder"]',
            instructions="1. Cook chicken, 2. Add spices, 3. Serve",
            created_by=self.user,
        )
        self.recipe2 = Recipe.objects.create(
            title="Vegetable Stir Fry",
            description="A healthy vegetable stir fry recipe",
            ingredients='["carrots", "broccoli", "bell peppers", "soy sauce"]',
            instructions="1. Chop vegetables, 2. Stir fry, 3. Serve",
            created_by=self.user,
        )

    def test_search_recipes_by_title(self):
        url = reverse("recipe-list-create") + "?search=Chicken"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Chicken Curry")

    def test_search_recipes_by_ingredients(self):
        url = reverse("recipe-list-create") + "?search=bell peppers"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Vegetable Stir Fry")


class RecipePaginationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        for i in range(20):
            Recipe.objects.create(
                title=f"Recipe {i}",
                description=f"Description for Recipe {i}",
                ingredients=f"Ingredient {i}",
                instructions=f"Instructions for Recipe {i}",
                created_by=self.user,
            )

    def test_recipe_pagination(self):
        url = reverse("recipe-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)  # Default page size is 10
        self.assertIn("next", response.data)

        next_url = response.data["next"]
        response = self.client.get(next_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("previous", response.data)


class RecipeCreateWithJsonIngredientsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.recipe_list_url = reverse("recipe-list-create")
        self.recipe_data = {
            "title": "Test Recipe",
            "description": "This is a test recipe",
            "ingredients": json.dumps({"onion": "0.5kg", "tomatoes": "0.25kg"}),
            "instructions": "Step 1, Step 2",
        }

    def test_create_recipe_with_json_ingredients(self):
        response = self.client.post(
            self.recipe_list_url, self.recipe_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().title, "Test Recipe")
        recipe = Recipe.objects.get()
        self.assertEqual(recipe.ingredients, '{"onion": "0.5kg", "tomatoes": "0.25kg"}')
        self.assertEqual(recipe.created_by, self.user)
