from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class MemberSerializer(ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'message',

        ]

    def validate(self, attrs):
        pass1 = attrs.get('password1', None)
        pass2 = attrs.get('password2', None)
        if pass2 != pass1:
            raise serializers.ValidationError("Password is not matching")
        return attrs

    def get_message(self, obj):
        return "Thanks for Registration"

    def validate_email(self, email):
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise serializers.ValidationError("Already exists User")
        return email

    def create(self, validated_data):
        firstname = validated_data.get('first_name')
        lastname = validated_data.get('last_name')
        username = validated_data.get('email')
        email = validated_data.get('email')
        password = validated_data.get('password1')
        obj = User.objects.create(username=username, email=email, first_name=firstname, last_name=lastname)
        obj.set_password(password)
        obj.is_staff = False
        obj.is_admin = False
        obj.save()
        return obj

    def update(self, instance, validated_data):
        password = validated_data.pop('password1', None)
        for key, value in validated_data.items():
            if key == 'email':
                setattr(instance, 'username', value)
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
