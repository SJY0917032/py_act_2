from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import resolve_url

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"
        
    follower_set = models.ManyToManyField("self", 
                                          blank=True,
                                          symmetrical=False,
                                          related_name="following_set",)
    
    
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(blank=True, validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")], max_length=13)
    gender = models.CharField(blank=True, choices=GenderChoices.choices, max_length=2)
    avatar = models.ImageField(blank=True, upload_to="accounts/avatar/%Y/%m/%d",
                               help_text="48px * 48px사이즈의 png/jpg 파일을 업로드해주세요.")
    # TODO
    # 커스텀Validator로 이미지 체크하기~ 48px48px사이즈 이렇게..
    # 업로드 되는 날짜의 년월일별로 폴더를 만드는게 리소스 활용이 좋다.
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar
        else:
            return resolve_url("pydenticon_image", self.username)
    
    def send_welcome_email(self):
        
        subject = render_to_string("accounts/welcome_email_subject.txt",{
            "user" : self,
        })
        content = render_to_string("accounts/welcome_email_content.txt",{
            "user" : self,
        })
        sender_mail = settings.WELCOME_EMAIL_SENDER
        send_mail(subject, content, sender_mail, [self.email], fail_silently=False)