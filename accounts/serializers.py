from django.contrib.auth import get_user_model
from django.db.models import DateTimeField
from django.utils.timezone import now
from rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
from rest_framework import serializers
from accounts.models import UserProfile, STAFF_TYPE, SocialAccount, Otp, ROLE_TYPE
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from event.models import EventSetting, Like, Comment, Follow

User = get_user_model()


class RegisterSerializer(DefaultRegisterSerializer):
    """

    """
    username = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)
    social_profile_pic = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(max_length=30, write_only=True)
    password2 = serializers.CharField(max_length=30, write_only=True)
    mobile = serializers.CharField(max_length=15, allow_null=True, allow_blank=True)
    dob = serializers.DateField(format='%m-%d-%Y', input_formats=['%m-%d-%Y'], allow_null=True)
    location = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    type = serializers.ChoiceField(choices=STAFF_TYPE, allow_null=True, allow_blank=True)
    profile_pic = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)
    profile_interest = serializers.BooleanField(required=False, allow_null=True)
    enabled_msg = serializers.BooleanField(required=False, allow_null=True)
    role = serializers.ChoiceField(choices=ROLE_TYPE)
    city = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    state = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    postal_code = serializers.CharField(max_length=6, allow_null=True, allow_blank=True)

    def custom_signup(self, request, user):
        mobile = self.validated_data.get('mobile', '')
        dob = self.validated_data.get('dob', '')
        location = self.validated_data.get('location', '')
        city = self.validated_data.get('city', '')
        state = self.validated_data.get('state', '')
        postal_code = self.validated_data.get('postal_code', '')
        type = self.validated_data.get('type', '')
        role = self.validated_data.get('role', '')
        profile_pic = self.validated_data.get('profile_pic', '')
        social_profile_pic = self.validated_data.get('social_profile_pic', '')
        profile_interest = self.validated_data.get('profile_interest', '')
        enabled_msg = self.validated_data.get('enabled_msg', '')
        user_profile = UserProfile(
            user=user,
            mobile=mobile,
            dob=dob,
            location=location,
            state=state,
            city=city,
            postal_code=postal_code,
            type=type,
            role=role,
            profile_pic=profile_pic,
            social_profile_pic=social_profile_pic,
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
            'role': self.validated_data.get('role', ''),
            'dob': self.validated_data.get('dob', ''),
            'location': self.validated_data.get('location', ''),
            'city': self.validated_data.get('city', ''),
            'state': self.validated_data.get('state', ''),
            'postal_code': self.validated_data.get('postal_code', ''),
            'profile_pic': self.validated_data.get('profile_pic', ''),
            'social_profile_pic': self.validated_data.get('social_profile_pic', ''),
            'profile_interest': self.validated_data.get('profile_interest', ''),
            'enabled_msg': self.validated_data.get('enabled_msg', '')
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """

    """
    dob = serializers.DateField(format='%m-%d-%Y', input_formats=['%m-%d-%Y',])

    is_profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('mobile', 'type', 'is_profile_pic', 'profile_pic', 'social_profile_pic', 'location',
                  'postal_code', 'city', 'state', 'enabled_msg', 'public_profile', 'invited', 'profile_groups',
                  'profile_interest', 'dob', 'role')

    def get_is_profile_pic(self, obj):
        if obj.user:
            try:
                get_user = User.objects.get(id=obj.user_id)
                is_social_user = SocialAccount.objects.get(email=get_user.email)
                if is_social_user:
                    if obj.is_profile_pic_updated:
                        return True
                    else:
                        return False
            except:
                return True


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    going = serializers.SerializerMethodField()
    interested = serializers.SerializerMethodField()
    commented = serializers.SerializerMethodField()
    profile = UserProfileSerializer()
    last_login = serializers.DateTimeField(default=now(), read_only=True)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile = validated_data.get('profile')

        if profile:
            profile_obj = UserProfile.objects.get(user__id=instance.pk)
            get_user = User.objects.get(id=instance.pk)
            is_social_user = SocialAccount.objects.filter(email=get_user.email)
            if is_social_user:
                if profile.get('profile_pic', profile_obj.profile_pic):
                    profile_obj.is_profile_pic_updated = True
                    profile_obj.profile_pic = profile.get('profile_pic', profile_obj.profile_pic)
                    profile_obj.social_profile_pic = profile.get('social_profile_pic', profile_obj.social_profile_pic)
                    profile_obj.mobile = profile.get('mobile', profile_obj.mobile)
                    profile_obj.location = profile.get('location', profile_obj.location)
                    profile_obj.postal_code = profile.get('postal_code', profile_obj.postal_code)
                    profile_obj.city = profile.get('city', profile_obj.city)
                    profile_obj.state = profile.get('state', profile_obj.state)
                    profile_obj.public_profile = profile.get('public_profile', profile_obj.public_profile)
                    profile_obj.enabled_msg = profile.get('enabled_msg', profile_obj.enabled_msg)
                    profile_obj.invited = profile.get('invited', profile_obj.invited)
                    profile_obj.profile_groups = profile.get('profile_groups', profile_obj.profile_groups)
                    profile_obj.profile_interest = profile.get('profile_interest', profile_obj.profile_interest)
                    profile_obj.dob = profile.get('dob', profile_obj.dob)
                    profile_obj.role = profile.get('role', profile_obj.role)
                else:
                    pass
            profile_obj.profile_pic = profile.get('profile_pic', profile_obj.profile_pic)
            profile_obj.social_profile_pic = profile.get('social_profile_pic', profile_obj.social_profile_pic)
            profile_obj.mobile = profile.get('mobile', profile_obj.mobile)
            profile_obj.location = profile.get('location', profile_obj.location)
            profile_obj.postal_code = profile.get('postal_code', profile_obj.postal_code)
            profile_obj.city = profile.get('city', profile_obj.city)
            profile_obj.state = profile.get('state', profile_obj.state)
            profile_obj.public_profile = profile.get('public_profile', profile_obj.public_profile)
            profile_obj.enabled_msg = profile.get('enabled_msg', profile_obj.enabled_msg)
            profile_obj.invited = profile.get('invited', profile_obj.invited)
            profile_obj.profile_groups = profile.get('profile_groups', profile_obj.profile_groups)
            profile_obj.profile_interest = profile.get('profile_interest', profile_obj.profile_interest)
            profile_obj.dob = profile.get('dob', profile_obj.dob)
            profile_obj.role = profile.get('role', profile_obj.role)

            profile_obj.save()
        return instance

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile', 'last_login', 'going',
                  'interested', 'commented')
        read_only_fields = ('email', )

    def get_going(self, obj):
        going = EventSetting.objects.filter(user_id=obj.id).count()
        return going

    def get_interested(self, obj):
        follow = Follow.objects.filter(created_by__id=obj.id).count()
        return follow

    def get_commented(self, obj):
        comment = Comment.objects.filter(created_by__id=obj.id)
        events = []
        count = 0
        for c in comment:
            if c.event_id not in events:
                events.append(c.event_id)
                count = count + 1
        return count


class UserSerializer(serializers.ModelSerializer):
    """

    """
    profile = UserProfileSerializer()

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
