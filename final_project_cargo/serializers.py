from django.contrib.auth import get_user_model

from rest_framework import serializers, status
from django.contrib.auth.models import Group, User
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from .models import Send_cargo


from django.core.validators import RegexValidator, validate_email


from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
Listt = ['+', '@', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


class User_infSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=10, validators=[RegexValidator(
        regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', message="Password must contains one digit from 0-9 ,must contains one lowercase and upper characters and length at least 10 characters ")], write_only=True)

    password2 = serializers.CharField(min_length=10, validators=[RegexValidator(
        regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', message="Password must contains one digit from 0-9 ,must contains one lowercase and upper characters, length at least 10 characters and Confirm Password must match with Password  ")], write_only=True)
    group = serializers.CharField()
    first_name = serializers.CharField(min_length=2, validators=[RegexValidator(
        regex=r'^[A-Za-z]+$', message=" Number not allow ")])
    last_name = serializers.CharField(min_length=2, validators=[RegexValidator(
        regex=r'^[A-Za-z]+$', message=" Number not allow ")])
    username = serializers.CharField(max_length=225, default="root")

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password must match!')
        return data

    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError('email is invalid')
        return email

    def create(self, validated_data):
        group_data = validated_data.pop('group')
        group, _ = Group.objects.get_or_create(name=group_data)
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        user = self.Meta.model.objects.create_user(**data)
        user.groups.add(group)
        user.save()
        return user

    class Meta:

        model = get_user_model()
        fields = (
            'id', 'username', 'email', 'password1', 'password2',
            'first_name', 'last_name', 'group',
            'image', 'phone_number'
        )
        extra_kwargs = {

            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=get_user_model().objects.all(),
                        message="This email already exist!"
                    )
                ]
            },
            'phone_number': {
                'validators': [
                    UniqueValidator(
                        queryset=get_user_model().objects.all(),
                        message="This phone_number already exist!"
                    ),  RegexValidator(
                        regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
                ]
            },
        }

        read_only_fields = ('id',)


class send_cargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Send_cargo
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated',)


class Nested_send_cargoSerializer(serializers.ModelSerializer):
    driver = User_infSerializer()
    rider = User_infSerializer()

    class Meta:
        model = Send_cargo
        fields = '__all__'
        depth = 1


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = User_infSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
        Serializer for password change endpoit.
        """
    old_password = serializers.CharField(
        required=True,)

    new_password = serializers.CharField(required=True, min_length=10, validators=[RegexValidator(
        regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', message="Password must contains one digit from 0-9 ,must contains one lowercase and upper characters and length at least 10 characters ")])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Your old password was entered incorrectly. Please enter it again.')
            )
        return value


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', ]
        extra_kwargs = {
            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=get_user_model().objects.all(),
                        message="This email already exist!"
                    )
                ]
            }
        }

    def update(self, instance, validated_data):

        instance.email = validated_data.get(
            'email', instance.email)
        instance.save()
        return instance


class UserUpdatephone(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['phone_number']
        phone_regex = RegexValidator(
            regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+9999999'. Up to 15 digits allowed.")
        model = get_user_model()
        fields = ['phone_number', ]
        extra_kwargs = {
            'phone_number': {
                'validators': [
                    UniqueValidator(
                        queryset=get_user_model().objects.all(),
                        message="This Phone Number already exist!"
                    ), phone_regex
                ]
            }
        }

    def update(self, instance, validated_data):

        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.save()
        return instance


class Userupdateimage(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['image']

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
