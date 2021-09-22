from django.contrib import admin
from django.urls import path,include
from .yasg import urlpatterns as doc_urls
from django.conf.urls import include, re_path
from django.conf import settings
from dreeapp.ckeditor_views import upload, browse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('dreeapp.urls')),
    path('ckeditor/upload/', login_required(upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(browse)), name='ckeditor_browse')]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
