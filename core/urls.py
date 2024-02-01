from django.urls import re_path
from django.urls import include


urlpatterns = [
    re_path(r'^api/v1/', include('apiv1.urls', namespace='api'))
]
