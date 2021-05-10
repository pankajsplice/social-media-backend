from django.contrib.auth import get_user_model
from django.db.models import DateTimeField
from django.utils.timezone import now
from rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
from rest_framework import serializers
from accounts.models import STAFF_TYPE
from accounts.models import UserProfile
from django.conf import settings

User = get_user_model()


class RegisterSerializer(DefaultRegisterSerializer):
    """

    """
    username = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    mobile = serializers.CharField(max_length=15)
    type = serializers.ChoiceField(choices=STAFF_TYPE)
    profile_pic = serializers.ImageField(required=False, allow_null=True)

    def custom_signup(self, request, user):
        mobile = self.validated_data.get('mobile', '')
        type = self.validated_data.get('type', '')
        profile_pic = self.validated_data.get('profile_pic', '')
        user_profile = UserProfile(
            user=user,
            mobile=mobile,
            type=type,
            profile_pic=profile_pic,
        )
        user_profile.save()

    def get_cleaned_data(self):
        if settings.USERNAME == 'email':
            username = self.validated_data.get('email', '')
        else:
            username = self.validated_data.get('mobile', '')
        return {
            'username': username,
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'mobile': self.validated_data.get('mobile', ''),
            'type': self.validated_data.get('type', ''),
            'profile_pic': self.validated_data.get('profile_pic', '')
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = UserProfile
        fields = ('mobile', 'type', 'profile_pic', 'location', 'profile_groups', 'profile_interest')


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
            profile_obj.profile_pic = profile.get('profile_pic', profile_obj.profile_pic)
            profile_obj.mobile = profile.get('mobile', profile_obj.mobile)
            profile_obj.location = profile.get('location', profile_obj.location)
            profile_obj.profile_groups = profile.get('profile_groups', profile_obj.profile_groups)
            profile_obj.profile_interest = profile.get('profile_interest', profile_obj.profile_interest)

            profile_obj.save()
        return instance

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile', 'last_login')
        read_only_fields = ('email', )