from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm
from .models import Post, Tag

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