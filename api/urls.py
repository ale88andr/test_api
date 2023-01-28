from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_urlpatterns


app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]
urlpatterns += doc_urlpatterns
