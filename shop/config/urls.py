from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "ЧистоДім — адмінка"
admin.site.site_title = "ЧистоДім"
admin.site.index_title = "Керування магазином"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("store.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
