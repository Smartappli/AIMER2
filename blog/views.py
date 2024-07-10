"""
This module handles the blog post views for a Django application, including
listing posts, displaying post details, sharing posts via email, and adding comments.

Functions and classes included in this module:

- post_list(request): Display a list of published blog posts with pagination.
- post_detail(request, year, month, day, post): Display the details of a single blog post.
- PostListView: A class-based view for listing published blog posts with pagination.
- post_share(request, post_id): Share a blog post via email.
- post_comment(request, post_id): Add a comment to a blog post.

Imports:
- send_mail: Sends an email using Django's email backend.
- EmptyPage, PageNotAnInteger, Paginator: Handles pagination of querysets.
- get_object_or_404, render: Utilities for retrieving objects and rendering templates.
- require_POST: Decorator for restricting views to POST requests.
- ListView: A class-based view for displaying a list of objects.
- CommentForm, EmailPostForm: Custom forms for adding comments and sharing posts.
- Post: The blog post model.
"""

from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Post


def post_list(request, tag_slug=None):
    """
    Display a list of published blog posts with pagination.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered template for the post list.
    """
    post_listing = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_listing = post_listing.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_listing, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def post_detail(request, year, month, day, post):
    """
    Display the details of a single blog post.

    Args:
        request: The HTTP request object.
        year: The year the post was published.
        month: The month the post was published.
        day: The day the post was published.
        post: The slug of the post.

    Returns:
        HttpResponse: The rendered template for the post detail.
    """
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
        id=post.id
    )
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )


class PostListView(ListView):
    """
    Alternative post list view using class-based views.
    """

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_share(request, post_id):
    """
    Share a blog post via email.

    Args:
        request: The HTTP request object.
        post_id: The ID of the post to be shared.

    Returns:
        HttpResponse: The rendered template for sharing a post.
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            )
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(
                subject,
                message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request,
        "blog/post/share.html",
        {"post": post, "form": form, "sent": sent},
    )


@require_POST
def post_comment(request, post_id):
    """
    Add a comment to a blog post.

    Args:
        request: The HTTP request object.
        post_id: The ID of the post to comment on.

    Returns:
        HttpResponse: The rendered template for adding a comment.
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = (
                Post.published.annotate(
                    similarity=TrigramSimilarity("title", query),
                )
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )

    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )
