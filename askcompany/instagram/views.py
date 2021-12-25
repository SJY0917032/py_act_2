from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .forms import CommentForm, PostForm
from .models import Post, Tag


@login_required
def index(request):
    # 3일까지의 타임라인만 보이게
    timesince = timezone.now() - timedelta(days=3)
    post_list = Post.objects.all()\
        .filter(
            Q(author=request.user) |
            Q(author__in=request.user.following_set.all())
        )\
        .filter(
            created_at__gte = timesince
        ) # 필터적용.
    
    suggested_user_list = get_user_model().objects.all()\
        .exclude(pk=request.user.pk)\
            .exclude(pk__in=request.user.following_set.all())[:3]
     
    return render(request, 'instagram/index.html', {
        "post_list" : post_list,
        "suggested_user_list" : suggested_user_list,
    })


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save() # M2M 관계는 실제 PK가 있어야만 저장이된다
            post.tag_set.add(*post.extract_tag_list()) # 그래서 post - tag는먼저 post save -> tag   
            messages.success(request, "포스팅을 저장했습니다.")
            return redirect(post)
    else:
        # GET
        form = PostForm()
        
    return render(request, "instagram/post_form.html",{
        "form" : form,
    })
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "instagram/post_detail.html", {
        "post" : post,
    })
    

def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)    
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # 실제 DB에 count 쿼리를 던진다.
    
    # 로그인이 돼있으면 유저객체 , 아니면 익명유저객체
    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else :
        is_follow = False
    
    return render(request, 'instagram/user_page.html', {
        "page_user" : page_user,
        'post_list' : post_list,
        'post_list_count' : post_list_count,
        'is_follow' : is_follow,
    })    
    
@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"포스팅#{post.pk} 좋아요했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)
    
@login_required
def post_dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"포스팅#{post.pk} 좋아요를 취소했습니다..")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required    
def post_comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
   
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "instagram/comment_form.html", {
        'form' : form
    })
    