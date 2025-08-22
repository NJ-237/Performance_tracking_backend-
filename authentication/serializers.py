from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile
from .models import Shift, BroyeurData, SecheurData, PortData, ExpeditionData


class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, min_length=6)
    service_location = serializers.CharField(write_only=True, required=False)
    position = serializers.CharField(write_only=True, required=False)
    employee_id = serializers.CharField(write_only=True, required=False)
    gender = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number', 'service_location', 'position', 'employee_id', 'gender',]
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)

    def create(self, validated_data):
        phone = validated_data.pop('phone_number', None)
        service_location = validated_data.pop('service_location', None)
        position = validated_data.pop('position', None)
        employee_id = validated_data.pop('employee_id', None)
        gender = validated_data.pop('gender', None)

        user = User.bjects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
            
        )

        Profile.objects.create(
            user=user,
            phone_number=phone or '',
            service_location=service_location,
            position=position,
            employee_id=employee_id,
            gender=gender
           
        )

        # if phone:
            # Profile.objects.create(user=user, phone_number=phone)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
    

    # serializers.py for the input values from the ReportSide.
class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')

class BroyeurDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BroyeurData
        fields = '__all__'

class SecheurDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecheurData
        fields = '__all__'

class PortDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortData
        fields = '__all__'

class ExpeditionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpeditionData
        fields = '__all__'
