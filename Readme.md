
## Setting up the Project

1.  Clone the Repository

    -   Clone the project repository from `https://github.com/naveens800/recipe_management.git`
2.  Create a Virtual Environment (Optional but Recommended)

    -   Create a new virtual environment using your preferred tool (e.g., `virtualenv`, `conda`, etc.).
    -   Activate the virtual environment.
3.  Install Dependencies

    -   Navigate to the project directory.
    -   Install the required dependencies by running:

        ```
        pip install -r requirements.txt

        ```

4.  Apply Database Migrations

    -   Run the following command to apply the initial database migrations:

        ```
        python manage.py migrate

        ```

## Running Tests

This project includes tests written in the `api/tests.py` module. To run the tests, follow these steps:

1.  Navigate to the Project Directory

    -   Ensure that you are in the project's root directory.
2.  Run Tests

    -   Run the following command to execute all tests:

        ```
        python manage.py test api

        ```

    -   This command will run all tests defined in the `api/tests.py` module.

## API Documentaion

1.  Register View

    -   URL: `/register/`
    -   HTTP Method: `POST`
    -   Description: This endpoint is used to register new users in the system.
    -   View Class: `RegisterView`
    -   Permissions: `AllowAny` (no authentication required)
    -   Serializer: `UserSerializer`
2.  Token Obtain Pair View

    -   URL: `/api/token/`
    -   HTTP Method: `POST`
    -   Description: This endpoint is used to obtain a new access and refresh JSON Web Token (JWT) pair for authentication.
    -   View Class: `TokenObtainPairView` (from `rest_framework_simplejwt.views`)
    -   Permissions: No authentication required
    -   Request Body: The request body should contain the user's credentials (e.g., `{"username": "myusername", "password": "mypassword"}`)
    -   Response: If the credentials are valid, the response will contain an access token and a refresh token.
3.  Token Refresh View

    -   URL: `/api/token/refresh/`
    -   HTTP Method: `POST`
    -   Description: This endpoint is used to refresh an existing JSON Web Token (JWT) access token using the refresh token.
    -   View Class: `TokenRefreshView` (from `rest_framework_simplejwt.views`)
    -   Permissions: No authentication required
    -   Request Body: The request body should contain the refresh token (e.g., `{"refresh": "myrefreshtoken"}`)
    -   Response: If the refresh token is valid, the response will contain a new access token.
1.  Recipe List/Create View
    -   URL: `/recipes/`
    -   HTTP Methods: `GET`, `POST`
    -   Description: This endpoint is used to list all available recipes and create new recipes.
    -   View Class: `RecipeListCreateView`
    -   Permissions: `IsAuthenticated` (authentication required)
    -   Serializer: `RecipeSerializer`
    -   Search Filters: `title`, `ingredients` (search filters are enabled for this endpoint)
    -   Search Query Parameter: `search`
    -   Example Usage: `/recipes/?search=chicken` (searches for recipes with "chicken" in the title or ingredients)
    -   Note: When creating a new recipe, the `perform_create` method is overridden to automatically set the `created_by` field to the current authenticated user.
5.  Recipe Retrieve/Update/Destroy View

    -   URL: `/recipes/<int:pk>/`
    -   HTTP Methods: `GET`, `PUT`, `PATCH`, `DELETE`
    -   Description: This endpoint is used to retrieve, update, and delete individual recipes.
    -   View Class: `RecipeRetrieveUpdateDestroyView`
    -   Permissions: `IsAuthenticated` and `IsOwnerOrReadOnly` (authentication required, and only the owner of the recipe can update or delete it)
    -   Serializer: `RecipeSerializer`
