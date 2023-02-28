from django.urls import path

from users.views.users import RegistrationView

urlpatterns = [
    path('users/reg', RegistrationView.as_view(), name='reg')
]
