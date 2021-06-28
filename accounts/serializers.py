from django.contrib.auth import get_user_model
from django.db.models import DateTimeField
from django.utils.timezone import now
from rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
from rest_framework import serializers
from accounts.models import UserProfile, STAFF_TYPE, SocialAccount, Otp
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm

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
    profile_interest = serializers.BooleanField(required=False, allow_null=True)
    enabled_msg = serializers.BooleanField(required=False, allow_null=True)

    def custom_signup(self, request, user):
        mobile = self.validated_data.get('mobile', '')
        type = self.validated_data.get('type', '')
        profile_pic = self.validated_data.get('profile_pic', '')
        profile_interest = self.validated_data.get('profile_interest', '')
        enabled_msg = self.validated_data.get('enabled_msg', '')
        user_profile = UserProfile(
            user=user,
            mobile=mobile,
            type=type,
            profile_pic=profile_pic,
            profile_interest=profile_interest,
            enabled_msg=enabled_msg,
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
            'profile_pic': self.validated_data.get('profile_pic', ''),
            'profile_interest': self.validated_data.get('profile_interest', ''),
            'enabled_msg': self.validated_data.get('enabled_msg', '')
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """

    """
    dob = serializers.DateField(input_formats=['%d-%m-%Y', ])

    class Meta:
        model = UserProfile
        fields = ('mobile', 'type', 'profile_pic', 'location', 'enabled_msg', 'public_profile', 'invited',
                  'profile_groups', 'profile_interest', 'dob')


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
            profile_obj.public_profile = profile.get('public_profile', profile_obj.public_profile)
            profile_obj.enabled_msg = profile.get('enabled_msg', profile_obj.enabled_msg)
            profile_obj.invited = profile.get('invited', profile_obj.invited)
            profile_obj.profile_groups = profile.get('profile_groups', profile_obj.profile_groups)
            profile_obj.profile_interest = profile.get('profile_interest', profile_obj.profile_interest)
            profile_obj.dob = profile.get('dob', profile_obj.dob)

            profile_obj.save()
        return instance

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile', 'last_login')
        read_only_fields = ('email', )


class UserSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')


class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = '__all__'


class OtpSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Otp
        fields = '__all__'


class PasswordResetOtpSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset otp.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    email = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}
        self.user = User._default_manager.get(email=attrs['email'])
        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        return self.set_password_form.save()
