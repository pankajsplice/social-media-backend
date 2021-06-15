from django.views.generic import TemplateView
from rest_framework import generics
from rest_social_auth.serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from accounts.serializers import SocialAccountSerializer
from accounts.models import SocialAccount
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


class SocialAccountLoginView(APIView):
    def post(self, request):
        token = request.data['token']
        social_data = SocialAccount.objects.filter(token=token)
        if social_data:
            SocialAccount.objects.filter(token=token).update(is_social_login=True)
            serializer = SocialAccountSerializer(social_data, many=True)
            return Response({'message': 'Token Exist', 'success': True, 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            social_serializer = SocialAccountSerializer(data=request.data)
            if social_serializer.is_valid():
                social_serializer.save()

                SocialAccount.objects.filter(token=token).update(is_social_login=True)
                serializer = SocialAccountSerializer(social_data, many=True)
                response = {'message': 'Token Saved', 'data': serializer.data}
                return Response(response, status=status.HTTP_200_OK)


class SocialAccountLogoutView(APIView):

    def post(self, request):
        SocialAccount.objects.filter(email=request.data['email']).update(is_social_login=False)
        query = SocialAccount.objects.filter(email=request.data['email'])
        serializer = SocialAccountSerializer(query, many=True)
        return Response({'message': 'Logged out Successfully', 'success': True, 'data': serializer.data})
