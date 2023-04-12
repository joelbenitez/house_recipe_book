from django.urls import path

from . import views

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe-home"),
    path("recipe/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipe/new/", views.RecipeCreateView.as_view(), name="recipe-create"),
    path("recipe/<int:pk>/update/", views.RecipeUpdateView.as_view(), name="recipe-update"),
    path("recipe/<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="recipe-delete"),
    path("user/<str:username>/", views.UserRecipeListView.as_view(), name="user-recipes"),
    path("about/", views.about, name="blog-about"),
]
