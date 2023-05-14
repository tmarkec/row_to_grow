from django.shortcuts import render
from .models import Blog
from django.views import generic, View
from django.core.paginator import Paginator
from django.contrib import messages


class BlogList(generic.ListView):
    """
    A view that displays the list of published blog posts.
    """
    model = Blog
    queryset = Blog.objects.filter(status=1).order_by("-created_on")
    template_name = "blog/blog.html"
    paginate_by = 6
