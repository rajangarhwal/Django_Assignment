from rest_framework import serializers
from .models import Advisor, Booking, User


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ['name', 'photo_url']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['time', 'user_id', 'advisor_id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password':{'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance