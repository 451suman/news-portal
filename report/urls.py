from django.urls import path

from report import views

app_name = "report"
urlpatterns = [
    path("users/", views.UserReportView.as_view(), name="users"),
    # path("posts/",views.PostPDFFile.as_view(), name="posts")
]