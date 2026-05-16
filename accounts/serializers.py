from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','email','password']

    def create(self, v_data):
        user = User.objects.create_user(
            username=v_data['username'],
            email=v_data['email'],
            password=v_data['password']
        )
        return user