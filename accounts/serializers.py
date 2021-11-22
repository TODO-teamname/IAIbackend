from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
            validators=[UniqueValidator(queryset=get_user_model().objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True, validators=[validate_password]);
    password2 = serializers.CharField(min_length=8, write_only=True);

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'], 
            password=validated_data['password'],
            )

        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']

        user.save()

        return user

