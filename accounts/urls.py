import djoser.views
from django.conf.urls import url
from django.contrib.auth import get_user_model
from rest_framework import routers
from django.urls import path, include
from accounts.views import SocialLoginView, UserTokenDetailView, SocialAccountLoginView, SocialAccountLogoutView
router = routers.DefaultRouter()
User = get_user_model()

router.register(r'user_list', djoser.views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    url(r'^token/$', SocialLoginView.as_view(), name='home_token'),
    path('current-social-user', UserTokenDetailView.as_view(),  name="current_user_token"),
    path('social-account-login/', SocialAccountLoginView.as_view(), name="social-login"),
    path('social-account-logout/', SocialAccountLogoutView.as_view(), name="social-logout"),

]
