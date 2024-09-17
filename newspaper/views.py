from django.contrib import messages
from urllib import request
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, View, DetailView
from newspaper.forms import ContactForm, CommentForm
from newspaper.models import Category, Post, Tag, Comment, Contact
from datetime import timedelta
from django.utils import timezone


# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )

        context["featured_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at", "-views_count")[1:4]

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False,
            status="active",
            published_at__gte=one_week_ago,  # gte means GREATER THAN onw week ago
        ).order_by("-published_at", "-views_count")[:7]

        context["recent_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:7]

        # context["tags"] = Tag.objects.all()[:12]
        # context["categories"] = Category.objects.all()[:3]

        # context["trending_posts"] = Post.objects.filter(
        #     published_at__isnull=False, status="active"
        # ).order_by("-views_count")[:3]
        # this is send direct from navigation.py

        return context


class AboutView(TemplateView):
    template_name = "aznews/about.html"


class PostListView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1  # ek page ma eouta matra dekhaune

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")


class PostByCategoryView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            category__id=self.kwargs["category_id"],
            # post model ko category__id = url_id
        ).order_by("-published_at")
        return query


class PostByTagView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            tag__id=self.kwargs["tag_id"],
            # post model ko tag__id = url_id
        ).order_by("-published_at")
        return query


class ContactView(View):
    template_name = "aznews/contacts.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Sucessfully Submitted your Query, We will contact you soon."
            )
            return redirect("contact")
        else:
            messages.error(
                request,
                "Cannot submit your query.Please make sure all fields are valid.",
            )
            return render(
                request,
                self.template_name,
                {"form": form},
            )


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        obj.views_count += 1

        obj.save()

        context["previous_post"] = (
            (
                Post.objects.filter(
                    published_at__isnull=False, status="active", id__lt=obj.id
                )
            )
            .order_by("-id")
            .first()
        )

        context["next_post"] = (
            (
                Post.objects.filter(
                    published_at__isnull=False, status="active", id__gt=obj.id
                )
            )
            .order_by("id")
            .first()
        )

        # context["comment"] = (
        #     Comment.objects.filter()
        # )

        return context

class CommentView(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post_id = request.POST["post"]
        if form.is_valid():
            form.save()
            return redirect("post-detail", post_id)

        post = Post.objects.get(pk=post_id)

        return render(
            request, "aznews/detail/detail.html", {"post": post, "form": form}
        )

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger


class PostSearchView(View):
    template_name = "aznews/list/list.html"

    def get(self, request, *args, **kwargs):
        query = request.GET["query"]
        post_list = Post.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query) )
            & Q(published_at__isnull=False)
        ).order_by("-published_at")

    #pagination start
        page= request.GET.get("page",1)
        paginate_by = 3
        paginator = Paginator(post_list, paginate_by, paginate_by)
        try:
            posts=paginator.page(page)
        except PageNotAnInteger:
            posts=paginator.page(1)

        #pagination end
        return render(request,self.template_name,{"page_obj":posts, "query":query})