from django.shortcuts import (
 render, get_object_or_404, HttpResponseRedirect, reverse
)
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
    paginate_by = 3


class BlogDetail(View):
    """
    A view that displays the details of a single blog post.
    """

    def get(self, request, slug, *args, **kwargs):
        queryset = Blog.objects.filter(status=1)
        blog = get_object_or_404(queryset, slug=slug)
        liked = False
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blog/blog_detail.html",
            {
                "blog": blog,
                "liked": liked,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Blog.objects.filter(status=1)
        blog = get_object_or_404(queryset, slug=slug)
        liked = False
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blog/blog_detail.html",
            {
                "blog": blog,
                "liked": liked,
            },
        )


class BlogLikes(View):
    """
    View to like a post
    """
    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)

        if blog.likes.filter(id=request.user.id).exists():
            blog.likes.remove(request.user)
        else:
            blog.likes.add(request.user)

        return HttpResponseRedirect(
                                    reverse(
                                            'blog:blog_detail',
                                            args=[slug]
                                             )
                                    )
