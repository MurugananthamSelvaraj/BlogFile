from django.urls import path

from . import views

urlpatterns = [
    # path("", views.starting_page, name="starting-page"),
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts", views.AllPostView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(),
         name="post-detail-page"),  # post/my-first-post
    path("read-later", views.RaedLaterView.as_view(), name="read-later")
]
