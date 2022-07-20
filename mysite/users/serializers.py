from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "is_active",
            "is_superuser",
        ]


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password_submit = serializers.CharField(required=True, write_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            "password",
            "password_submit",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_submit"]:
            raise serializers.ValidationError("Passwords unmatched")
        return super().validate(attrs)

    def create(self, validated_data, **kwargs):
        validated_data.pop("password_submit")
        return super().create(**validated_data)
