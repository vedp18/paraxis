from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostCreateForm
from .models import Post
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.

# This view is for creating new post
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post created successfully')
            return redirect('/account/me')
    elif request.GET:
        form = PostCreateForm(data=request.GET)
    else:
        form = PostCreateForm(initial={'url': request.GET.get('url','')})
    return render(request, 'post/create.html', {'section': 'posts', 'form': form})


# This view is for showing post with in detail
def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    return render(request, 'post/post_detail.html', 
                  {'section': 'post', 'post': post})


# This view is for likes 
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            
            liked_user_html = render_to_string('post/partial/liked_users.html', {'post': post})
            return JsonResponse({
                'status': 'ok',
                'liked_users_html': liked_user_html
            })
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})
