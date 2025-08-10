from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostCreateForm
from .models import Post


# Create your views here.
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
    
def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    return render(request, 'post/post_detail.html', 
                  {'section': 'post', 'post': post})

