from django.db import models
from django.conf import settings
from django.urls import reverse
import re

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

# user
# -> Post.objects.filter(author=user)
# -> user.my_post_set.all()
class Post(BaseModel):
    # FK로 유저를 가져온다 -> settings에 세팅된 유저모델
    author = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               on_delete=models.CASCADE, 
                               related_name='my_post_set')
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.CharField(max_length=500)
    # 태그가 없는경우도 있기에 blank True
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)
    
    # 좋아요 구현
    # 포스팅과 유저간의 릴레이션쉽을 만들어야한다 m2m
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name="like_post_set")
        
    def __str__(self):
        return self.caption
        
    def extract_tag_list(self):
        tag_name_list =  re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list
    
    def get_absolute_url(self):
        return reverse('instagram:post_detail', args=[self.pk])
    
    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()
    
    class Meta:
        ordering = ['-id']
    
class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()
    
    class Meta:
        ordering = ['-id']
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

        
    def __str__(self):
        return self.name