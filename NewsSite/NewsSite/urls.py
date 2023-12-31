from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


handler404 = 'main.views.custom_404'
handler403 = 'main.views.custom_403'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]