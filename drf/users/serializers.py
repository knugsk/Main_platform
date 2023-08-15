from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('stu_id', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            stu_id=validated_data['stu_id'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    stu_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(
            request=self.context.get('request'),
            username=data['stu_id'],
            password=data['password']
        )
        if user:
            if not user.is_active:
                raise serializers.ValidationError({"error": "사용자가 아직 활성화되지 않았습니다."})
            data['user'] = user
            return data
        raise serializers.ValidationError({"error": "제공된 자격 증명으로 로그인할 수 없습니다."})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('stu_id', 'first_name', 'last_name')