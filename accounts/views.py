from django.template.loader import render_to_string
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_social_auth.serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from accounts.serializers import SocialAccountSerializer, OtpSerializer, PasswordResetOtpSerializer
from accounts.models import SocialAccount
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from django.core.mail import send_mail, EmailMultiAlternatives
from local_mingle_backend.settings import DEFAULT_FROM_EMAIL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from accounts.models import Otp
from accounts.models import UserProfile

User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

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
    permission_classes = (AllowAny,)

    def post(self, request):
        token = request.data['token']
        email = request.data.get('email', None)
        social_data = SocialAccount.objects.filter(token=token)
        if social_data:
            SocialAccount.objects.filter(token=token).update(is_social_login=True)
            serializer = SocialAccountSerializer(social_data, many=True)
            return Response({'message': 'Token Exist', 'success': True, 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            response = None
            user_exists = None
            if email:
                user_exists = User.objects.filter(email=email)

            if user_exists:
                social_data = SocialAccount.objects.filter(token=token)
                SocialAccount.objects.filter(token=token).update(is_social_login=True)
                serializer = SocialAccountSerializer(social_data, many=True)
                return Response({'message': 'Token already Exist', 'success': True, 'data': serializer.data},
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
    permission_classes = (AllowAny,)

    def post(self, request):
        SocialAccount.objects.filter(email=request.data['email']).update(is_social_login=False)
        query = SocialAccount.objects.filter(email=request.data['email'])
        serializer = SocialAccountSerializer(query, many=True)
        return Response({'message': 'Logged out Successfully', 'success': True, 'data': serializer.data})


class SendOtpApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email', '')
        mobile = request.data.get('mobile', '')

        if email != '':
            user = User.objects.get(email=email)
            otp = random.randint(1000, 9999)
            serializer = OtpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(otp=otp)
            subject = 'LocalMingle Forgot Password Otp'
            text_content = 'LocalMingleR Forgot Password Otp'
            # message = f"Hello {user.first_name} {user.last_name} \n Your Forgot Password Otp is {otp}"
            html_content = render_to_string('mail/otp.html', {
                "user": f"{user.first_name} {user.last_name}",
                "otp": otp,
            })
            msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [email])
            msg.attach_alternative(html_content, "text/html")

            try:
                msg.send()
                # send_mail(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=[email],
                #           fail_silently=True)
            except:
                return Response({'message': 'Email not send'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'An otp has been sent to your email'}, status=status.HTTP_200_OK)
        elif mobile != '':
            user = User.objects.get(email=mobile)
            otp = random.randint(1000, 9999)
            serializer = OtpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(otp=otp)
            title = 'LocalMingle Forgot Password Otp'
            body = f"Hello {user.first_name} {user.last_name} \n Your Forgot Password Otp is {otp}"

            # Find your Account SID and Auth Token at twilio.com/console
            # and set the environment variables. See http://twil.io/secure
            account_sid = TWILIO_ACCOUNT_SID
            auth_token = TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            try:
                message = client.messages.create(body=body,
                                                 from_='+13237451893',
                                                 to='+91' + mobile)
                print(message.sid)
            except:
                return Response({'message': 'Sms not send'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'An otp has been sent to your mobile'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email or Mobile can not be blank.'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email', '')
        mobile = request.data.get('mobile', '')
        if email != '':
            otp_obj = Otp.objects.get(email=request.data['email'], verify=False)
            if otp_obj:
                if int(request.data['otp']) == otp_obj.otp:
                    serializer = OtpSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    otp_obj.verify = True
                    otp_obj.save()
                    return Response({'message': 'Your otp is verified successfully', 'status': status.HTTP_200_OK})
                else:
                    return Response({'message': 'You have entered wrong otp.', 'status': status.HTTP_400_BAD_REQUEST})
            else:
                return Response({'message': 'Please enter valid email to verify otp',
                                 'status': status.HTTP_400_BAD_REQUEST})
        elif mobile != '':
            otp_obj = Otp.objects.get(email=request.data['mobile'], verify=False)
            if otp_obj:
                if int(request.data['otp']) == otp_obj.otp:
                    serializer = OtpSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    otp_obj.verify = True
                    otp_obj.save()
                    return Response({'message': 'Your otp is verified successfully', 'status': status.HTTP_200_OK})
                else:
                    return Response({'message': 'You have entered wrong otp.', 'status': status.HTTP_400_BAD_REQUEST})
            else:
                return Response({'message': 'Please enter valid mobile number to verify otp',
                                 'status': status.HTTP_400_BAD_REQUEST})

        else:
            return Response({'message': 'Email or Mobile can not be blank.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetOtpView(GenericAPIView):
    """
    Password reset otp is verified, therefore
    this resets the user's password.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetOtpSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetOtpView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password has been reset with the new password."}
        )


class UserPrivateMessageStatus(APIView):

    def post(self, request):
        user = request.data.get('user')
        if user:
            get_user = User.objects.get(id=user)
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.enabled_msg:
                return Response({'private_message': 'enabled'}, status=200)
            else:
                return Response({'private_message': 'disabled'}, status=400)
        else:
            return Response({'error': 'Please add user as input'}, status=400)

