from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from users.serializers.nested.profile import ProfileSerializer, ProfileUpdateSerializer

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError('Пользователь с таким email уже зарегестрирован.')
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('current_password', 'new_password')

    def validate(self, attrs):
        user = self.instance
        current_password = attrs.pop('current_password')
        if not user.check_password(current_password):
            raise ParseError('Текущий пароль не верен!')
        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password')
        instance.set_password(new_password)
        instance.save()
        return instance


class MeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'is_superuser',
            'first_name',
            'last_name',
            'date_joined',
            'username',
            'phone_number',
            'email',
            'profile',
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'phone_number',
            'email',
            'profile',
        )

    def update(self, instance, validated_data):
        # проверка, существуют ли данные профиля в запросе
        profile_data = validated_data.pop('profile') if 'profile' in validated_data else None

        # начало транзакции
        with transaction.atomic():
            # обновление данных пользователя
            instance = super().update(instance, validated_data)
            # обновление данных профиля
            if profile_data:
                self._update_profile(instance.profile, profile_data)

        return instance

    def _update_profile(self, profile, data):
        # for key, value in data.items():
        #     if hasattr(profile, key):
        #         setattr(profile, key, value)
        # profile.save()
        profile_serializer = ProfileUpdateSerializer(
            instance=profile, data=data, partial=True
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
