from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView
import hashlib
from django_pydenticon.views import image as pydenticon_image

# @login_Required
# def root(request):
#     return render(request, 'root.html')
def index(request):
    email_hash = hashlib.md5(request.user.email.encode('utf-8').strip().lower()).hexdigest()
    return email_hash

urlpatterns = [
    path('identicon/image/<path:data>/', pydenticon_image,name='pydenticon_image'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', login_required(TemplateView.as_view(template_name='root.html')), name='root'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)
    
    
