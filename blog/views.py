from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 每页显示3篇文章
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出总页数就返回最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month,
                             publish__day=day)
    # 列出文章对应的所有活动的评论
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 通过表单直接创建新数据对象，但是不要保存到数据库中
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章
            new_comment.post = post
            # 将评论数据对象写入数据库
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


def index(request):
    return render(request, 'index.html', {})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # 通过id 获取 post 对象
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == "POST":
        # 表单被提交
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 表单字段通过验证
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            # 这里的第三个参数，必须与settings.py中配置的EMAIL_HOST_USER的值是一样的，否则发送邮件失败
            send_mail(subject, message, 'stduser@126.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
