from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Count


def new(request):
    context = {
            'form': PostForm(initial={'user': request.user})
    }
    return render(request, 'posts/new.html', context)


def create(request):
    if request.method == "POST":
       form = PostForm(request.POST, request.FILES or None)
       if form.is_valid():
           form.save()
    return redirect('home')


def edit(request, id):
    post = get_object_or_404(Post, pk=id)
    if 'id' is not None:
        context = {
            'post': post,
            'form': PostForm(instance=post)
        }
        return render(request, 'posts/edit.html', context)


def update(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=post)
        if form.is_valid():
            form.save()

        return redirect('home')


def delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('home')


def create_comment(request, post_id):
    if request.method == "POST":
        user = request.user
        if user.is_anonymous:
            return redirect('account_login')
        post = get_object_or_404(Post, pk=post_id)
        message = request.POST.get('message')
        Comment.objects.create(user=user, post=post, message=message)
        return redirect('home')


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('home')


def like_toggle(request, post_id):
    user = request.user
    if user.is_anonymous:
        return redirect('account_login')
    post = get_object_or_404(Post, pk=post_id)
    
    is_like = user in post.likes.all()
    
    if is_like:
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect('home')
    