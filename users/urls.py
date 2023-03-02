from django.urls import path

from users.views.users import RegistrationView, ChangePasswordView

urlpatterns = [
    path('users/reg', RegistrationView.as_view(), name='reg'),
    path('users/change-passwd', ChangePasswordView.as_view(), name='change_passwd'),
]
