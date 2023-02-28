from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_urlpatterns
from users.urls import urlpatterns as user_urls


app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urlpatterns
urlpatterns += user_urls
