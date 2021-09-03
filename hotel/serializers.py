from django.db.models import fields
from rest_framework import serializers
from .models import Room, Booking
from rest_framework import serializers
from django.contrib.auth.models import User


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number']

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['category'] = CategorySerializer(instance.category).data
    #     return rep

class BookingListSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    roomno = RoomListSerializer(many=False, read_only=True)


    class Meta:
        model = Booking
        # fields = ['id','username', 'user','room','roomno', 'check_in', 'check_out']
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['room'] = RoomListSerializer(instance.room).data
        return rep



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4),

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']


