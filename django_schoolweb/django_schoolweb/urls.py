
from django.urls import path
from django_schoolweb.settings import MEDIA_ROOT
from django.conf.urls import url,include
from django.views.static import serve

urlpatterns = [

    path('admin/', include("adminuser.urls")),
    path('', include("school.urls")),
    url(r"^media/(?P<path>.*)$", serve, {"document_root": MEDIA_ROOT}),
]
