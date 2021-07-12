import djoser.views
from django.conf.urls import url
from django.contrib.auth import get_user_model
from rest_framework import routers
from django.urls import path, include
from accounts.views import SocialLoginView, UserTokenDetailView, SocialAccountLoginView, SocialAccountLogoutView,\
    PasswordResetOtpView, SendOtpApiView, VerifyOtpApiView, UserPrivateMessageStatus

router = routers.DefaultRouter()
User = get_user_model()

router.register(r'user_list', djoser.views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    url(r'^token/$', SocialLoginView.as_view(), name='home_token'),
    path('current-user/', UserTokenDetailView.as_view(),  name="current_user_token"),
    path('social-account-login/', SocialAccountLoginView.as_view(), name="social-login"),
    path('social-account-logout/', SocialAccountLogoutView.as_view(), name="social-logout"),
    path('send-otp/', SendOtpApiView.as_view(), name="send-otp"),
    path('verify-otp/', VerifyOtpApiView.as_view(), name="verify-otp"),
    path('password-reset/', PasswordResetOtpView.as_view(), name="password-reset"),
    path('private-msg-status/', UserPrivateMessageStatus.as_view(), name="private-msg-status"),

]
