from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostCreateForm
from .models import Post
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import redis
from django.conf import settings
# Connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)




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



# helper function for post_detail view
def _viewer_id(request):
    # Prefer authenticated user id; otherwise a stable session id
    if request.user.is_authenticated:
        return f"user:{request.user.pk}"
    if not request.session.session_key:
        request.session.save()  # ensure a session exists
    return f"anon:{request.session.session_key}"

# This view is for showing post with in detail
def post_detail(request,username, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    
    viewers_key = f'post:{post.id}:viewers'
    viewer = _viewer_id(request)

    # Add this viewer to the set
    r.sadd(viewers_key, viewer)

    # increment total post views by 1
    total_views = r.scard(viewers_key)

    return render(request, 'post/post_detail.html', 
                  {'section': 'post', 
                   'post': post,
                   'total_views':total_views})


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
                post.users_liked.add(request.user)
            else:
                post.users_liked.remove(request.user)
            
            users_liked_html = render_to_string('post/partial/users_liked.html', {'post': post})
            return JsonResponse({
                'status': 'ok',
                'users_liked_html': users_liked_html
            })
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})



# This view is for posts infinite scroll like explore posts
from django.db.models import Count
@login_required
def post_list(request): 
    all_posts = Post.objects.all()
    # posts_by_popularity = Post.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')  # expensive way
    posts_by_popularity = Post.objects.order_by('-likes')    # cheaper way
    paginator = Paginator(posts_by_popularity, 8)
    page = request.GET.get('page')
    posts_only = request.GET.get('posts_only')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the 1st page
        posts = paginator.page(1)
    except EmptyPage:
        if posts_only:
            # If AJAX request and page out range
            # return an Empyt Page
            return HttpResponse('')
        # If page out of range, return the last page
        posts = paginator.page(paginator.num_pages)

    keys = [f"post:{post.id}:viewers" for post in posts]
    viewers = r.mget(keys)

    pipe = r.pipeline()
    for post in posts:
        pipe.scard(f"post:{post.id}:viewers")
    
    view_counts = pipe.execute()

    for post, count in zip(posts, view_counts):
        post.total_views = count

    if posts_only:
        return render(request, 'post/post_list.html', {'section': 'posts', 'posts': posts})

    return render(request, 'post/list.html', {'section': 'posts', 'posts': posts})