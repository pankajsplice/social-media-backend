from django.views.generic import TemplateView
from rest_framework import generics
from rest_social_auth.serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()


class SocialLoginView(TemplateView):
    template_name = 'account/login_with_social.html'


class UserTokenDetailView(generics.RetrieveAPIView):
    permission_classes = IsAuthenticated,
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer
    model = get_user_model()

    def get_object(self, queryset=None):
        return self.request.user
