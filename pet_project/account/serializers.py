from datetime import date

from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers

from account.models import Profile, UserAuth


class UserAuthSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAuth
        fields = ['email', 'password', 'password_confirm']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data.pop('password_confirm')
        user = UserAuth.objects.create(**validated_data)
        return user

    def validate(self, attrs):
        print(attrs)
        if 'password' in attrs.keys():
            if attrs.get('password') != attrs.get('password_confirm'):
                raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def validate_email(self, email):
        if UserAuth.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"Пользователь с таким адресом электронной почты уже зарегистрирован"})
        return email


class ProfileSerializer(serializers.ModelSerializer):
    auth = UserAuthSerializer()

    class Meta:
        model = Profile
        fields = ['sex', 'name', 'birthday', 'about', 'i_search', 'auth']

    @transaction.atomic
    def create(self, validated_data):
        auth_data = validated_data.pop('auth')
        
        auth_serializer = UserAuthSerializer(data=auth_data)
        auth_serializer.is_valid(raise_exception=True)
        user_auth = auth_serializer.save()

        user_profile = Profile.objects.create(auth=user_auth, **validated_data)
        return user_profile

    def validate_birthday(self, birthday):
        dif_date = date.today() - birthday
        age = int(dif_date.days / 365)
        if age < 18:
            raise serializers.ValidationError({"Вам еще нет 18."})
        return birthday
