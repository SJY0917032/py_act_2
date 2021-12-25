from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import PostForm
from .models import Post, Tag

@login_required
def index(request):
    return render(request, 'instagram/index.html', {
        
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
    return render(request, 'instagram/user_page.html', {
        "page_user" : page_user,
        'post_list' : post_list,
        'post_list_count' : post_list_count
    })    