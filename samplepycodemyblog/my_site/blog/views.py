# from datetime import date

from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views import View

from .models import Post
from .forms import CommentForm

# Create your views here.

# all_posts = [
 
# ]

# def get_date(post):
#  return post['date']

class StartingPageView(ListView):
  template_name = "blog/index.html"
  model = Post
  ordering = ["-date"]
  context_object_name = "posts"

  def get_queryset(self):
    queryset = super().get_queryset()
    data = queryset[:3]
    return data

# def starting_page(request):
#   latest_posts = Post.objects.all().order_by("-date")[:3]
#   # sorted_posts = sorted(all_posts, key=get_date)
#   # latest_posts = sorted_posts[-3:]
#   return render(request, "blog/index.html", {
#    "posts": latest_posts
#  })

class AllPostView(ListView):
  template_name = "blog/all-posts.html"
  model = Post
  ordering = ["-date"]
  context_object_name = "all_posts"

# def posts(request):
#   all_posts = Post.objects.all().order_by("-date")
#   return render(request,"blog/all-posts.html", {
#     "all_posts": all_posts
#   })

class SinglePostView(View):
    #step 2
  # template_name = "blog/post-details.html"
  # model = Post

  def get(self,request,slug):
    post = Post.objects.get(slug=slug)
    context = {
      "post": post,
      "post-tags": post.tags.all(),
      "comment_form": CommentForm(),
      "comments": post.comments.all().order_by("-id")
    }
    return render(request, "blog/post-details.html", context)


  def post(self, request, slug):
    comment_form = CommentForm(request.POST)
    post = Post.objects.get(slug=slug)

    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.post = post
      comment.save()

      return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
    
    context = {
      "post": post,
      "post-tags": post.tags.all(),
      "comment_form": CommentForm(),
      "comments": post.comments.all().order_by("-id")
    }
    return render(request, "blog/post-details.html", context)

 # step 2
  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs)
  #   context["post_tags"] = self.object.tags.all()
  #   context["comment_form"] = CommentForm()
  #   return context

# step 1
# def post_detail(request, slug):
#   # identified_post = next(post for post in all_posts if post['slug'] == slug) 
#   identified_post = get_object_or_404(Post, slug=slug)
#   return render(request, "blog/post-details.html", {
#     "post": identified_post,
#     "post_tags" : identified_post.tags.all()
#  })

class RaedLaterView(View):
  def post(self, request):
     stored_posts = request.session.get("stored_posts")

     if stored_posts is None:
       stored_posts = []

       post_id = int(request.POST["post_id"])
       
       if post_id not in stored_posts:
        stored_posts.append(post_id)

        return HttpResponseRedirect("/")