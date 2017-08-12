from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(
        source='user_profile_img',
        default="profile/default.png",
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ('profile_img', 'nickname', 'age', 'gender', 'update_at')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    user_status = serializers.IntegerField(
        source='users.user_status',
        required=False
    )
    status_changed = serializers.DateTimeField(
        source='users.update_at',
        required=False
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)

        user = User.objects.create_user(
            user_acc=validated_data.get('user_acc'),
            password=validated_data.get('password'))
        user.profile.nickname = profile_data.get('nickname')
        user.profile.age = profile_data.get('age')
        user.profile.gender = profile_data.get('gender')
        user.save()

        return user

    class Meta:
        model = User
        fields = ('userid', 'user_acc', 'password', 'user_status', 'status_changed', 'profile', 'create_at')


    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile', None)
    #     hello = profile_data.get('nickname')
    #     print(hello)
    #     user = super(UserSerializer, self).create(validated_data)
    #     self.create_or_update_profile(user, profile_data)
    #     return user
    #
    # def create_or_update_profile(self, user, profile_data):
    #     profile, created = UserProfile.objects.get_or_create(userid=user, defaults=profile_data)
    #     if not created and profile_data is not None:
    #         super(UserSerializer, self).update(profile, profile_data)





