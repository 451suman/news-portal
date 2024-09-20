from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"tags", views.TagViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"posts", views.PostViewSet, basename="api-posts")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("post-publish/", views.PostPublishView.as_view(), name="post-publish-api"),
    path(
        "post-by-category/<int:category_id>/",
        views.PostListByCategoryViewSet.as_view(),
        name="post_by_category_api",
    ),
    path(
        "post-by-tag/<int:tag_id>/",
        views.PostListByTagViewSet.as_view(),
        name="post_by_tag_api",
    ),
]
