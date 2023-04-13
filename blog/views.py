from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.defaults import (
    bad_request,
    page_not_found,
    permission_denied,
    server_error,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Recipe

# Create your views here.

motd = "This site will undergo maintenance on 4/15 at 2:00 AM UTC"


def home(request):
    context = {"recipes": Recipe.objects.all()}
    if motd:
        messages.info(request, f"{motd}")
    return render(request, "blog/home.html", context)


class RecipeListView(LoginRequiredMixin, ListView):

    model = Recipe
    # New template replacing <app>/<model>_<view_type>.html
    template_name = "blog/home.html"
    context_object_name = "recipes"
    # In order to sort by date_posted, date_posted will reverse
    ordering = ["-date_posted"]
    paginate_by = 5


class UserRecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    # New template replacing <app>/<model>_<view_type>.html
    template_name = "blog/user_recipes.html"
    context_object_name = "recipes"
    # In order to sort by date_posted, date_posted will reverse
    paginate_by = 5

    def get_queryset(self):
        """Returns posts that belong to the current user"""
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Recipe.objects.filter(author=user).order_by("-date_posted")


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ["title", "content", "recipe_link", "recipe_book"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ["title", "content", "recipe_link", "recipe_book"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = "/"

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})


def handler404(request, exception, template_name="404.html"):
    response = page_not_found(template_name)
    response.status_code = 404
    return response


def handler403(request, exception, template_name="403.html"):
    response = permission_denied(template_name)
    response.status_code = 403
    return response


def handler500(request, exception, template_name="500.html"):
    response = server_error(template_name)
    response.status_code = 500
    return response


def handler400(request, exception, template_name="400.html"):
    response = bad_request(template_name)
    response.status_code = 400
    return response
