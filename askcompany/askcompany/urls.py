from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django_pydenticon.views import image as pydenticon_image

# @login_Required
# def root(request):
#     return render(request, 'root.html')

urlpatterns = [
    path('identicon/image/<path:data>/', pydenticon_image,name='pydenticon_image'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('instagram.urls')),
    path('', RedirectView.as_view(pattern_name='instagram:index'), name='root'),
    # pattern_name -> 빈문자열로 온다면 인스타그램의 index로 가겟다.
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)
    
    
