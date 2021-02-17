from django.contrib.auth import get_user_model
from django.db.models import DateTimeField
from django.utils.timezone import now
from rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
from rest_framework import serializers

from accounts.models import UserProfile

User = get_user_model()


class RegisterSerializer(DefaultRegisterSerializer):
    """

    """
    username = serializers.CharField(max_length=15)
    first_name = serializers.CharField(max_length=15)
    last_name = serializers.CharField(max_length=15)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    mobile = serializers.CharField(max_length=15)

    def custom_signup(self, request, user):
        mobile = self.validated_data.get('mobile', '')
        user_profile = UserProfile(
            user=user,
            mobile=mobile
        )
        user_profile.save()


    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'mobile': self.validated_data.get('mobile', '')
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = UserProfile
        fields = ('mobile')


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    profile = UserProfileSerializer()
    last_login = serializers.DateTimeField(default=now(), read_only=True)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile = validated_data.get('profile')

        if profile:
            profile_obj = UserProfile.objects.get(user__id=instance.pk)
            # profile_obj.mobile = profile.get('mobile', profile_obj.mobile)

            profile_obj.save()
        return instance

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile', 'last_login')
        read_only_fields = ('email', )