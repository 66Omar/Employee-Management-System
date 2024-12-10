from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authentication import authenticate
import re

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "re_password",
            "username",
            "address",
            "mobile_number",
        ]

    def validate_mobile_number(self, value):
        if not re.match(r"^\+?1?\d{9,15}$", value):
            raise serializers.ValidationError("Invalid mobile number format.")
        return value

    def create(self, validated_data):
        if (validated_data["password"] != validated_data["re_password"]) or (
            not validated_data["password"] or not validated_data["re_password"]
        ):
            raise serializers.ValidationError({"password": "Passwords mismatch"})
        del validated_data["re_password"]
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password", style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "Invalid email or password.", code="authorization"
                )
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'.", code="authorization"
            )

        attrs["user"] = user
        return attrs



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'address', 'mobile_number']