from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import BlogPost


def post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog2/post/list.html', {'posts': posts})


def post_detail(request, title):
    # post = get_object_or_404(BlogPost, publish__year=year, publish__month=month,
    #                          publish__day=day)
    # return render(request, 'blog2/post/detail.html', {'post': post})
    post = get_object_or_404(BlogPost, title=title)
    # post = BlogPost.objects.filter(title=title)
    return render(request, 'blog/post/detail.html', {'post': post})
