from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = Group.description
    context = {
        'group': group,
        'posts': posts_list,
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_count = author.posts.count()
    title = f'Профиль пользователя {author}'

    paginator = Paginator(author.posts.all(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'title': title,
        'posts_count': posts_count,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    author = get_object_or_404(Post, id=post_id)
    post = Post.objects.get(pk=post_id)
    posts_count = Post.objects.all().count()
    title = f'Пост {author}'
    context = {
        'author': author,
        'post': post,
        'posts_count': posts_count,
        'title': title,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('posts:profile', request.user.username)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    is_form_edit = True
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None,
                        files=request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('posts:post_detail', post_id)
        form = PostForm(instance=post)

        return render(request, 'posts/post_create.html',
                      context={'form': form,
                               'is_form_edit': is_form_edit,
                               'post': post})
    else:
        return redirect('posts:post_detail')
