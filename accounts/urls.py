import djoser.views
from django.conf.urls import url
from django.contrib.auth import get_user_model

from accounts.views import ProfileViewSet

User = get_user_model()

urlpatterns = [
    url(r'^me/$', djoser.views.UserView.as_view(), name='user'),
    # url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^activate/$', djoser.views.ActivationView.as_view(), name='activate'),
    url(r'^{0}/$'.format(User.USERNAME_FIELD), djoser.views.SetUsernameView.as_view(), name='set_username'),
    url(r'^password/$', djoser.views.SetPasswordView.as_view(), name='set_password'),
    url(r'^password/reset/$', djoser.views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/confirm/$', djoser.views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url(r'^login/$', djoser.views.LoginView.as_view(), name='login'),
    # url(r'^logout/$', djoser.views.LogoutView.as_view(), name='logout'),
    # url(r'^$', djoser.views.RootView.as_view(urls_extra_mapping={'login': 'login', 'logout': 'logout'}), name='root'),
]
