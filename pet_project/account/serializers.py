from datetime import date

from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers

from account.models import Profile, UserAuth


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    sex = serializers.CharField(max_length=1)
    i_search = serializers.CharField(max_length=1)
    name = serializers.CharField(max_length=20)
    birthday = serializers.EmailField()
    about = serializers.CharField(max_length=250)
    profile_photo = serializers.ImageField()
    auth = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def validate_birthday(self, birthday):
        dif_date = date.today() - birthday
        age = int(dif_date.days / 365)
        if age < 18:
            raise serializers.ValidationError({"Возраст должен быть > 18"})
        return birthday


class RegisterUserSerializer(serializers.Serializer):
    sex = serializers.CharField(max_length=1)
    i_search = serializers.CharField(max_length=1)
    name = serializers.CharField(max_length=20)
    birthday = serializers.DateField()
    email = serializers.EmailField(source='auth.email')
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    @transaction.atomic
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = UserAuth.objects.create(
            password=validated_data['password'],
            email=validated_data['auth']['email']
        )
        user_profile = Profile.objects.create(
            name=validated_data['name'],
            birthday=validated_data['birthday'],
            sex=validated_data['sex'],
            i_search=validated_data['i_search'],
            auth_id=user.id,
        )
        return user_profile

    def validate_birthday(self, birthday):
        dif_date = date.today() - birthday
        age = int(dif_date.days / 365)
        if age < 18:
            raise serializers.ValidationError({"Вам еще нет 18."})
        return birthday

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def validate_email(self, email):
        if UserAuth.objects.filter(email=email).exists():
            raise serializers.ValidationError({"Пользователь с таким адресом электронной почты уже зарегистрирован"})
        return email
