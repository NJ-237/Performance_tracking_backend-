from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile
from .models import Shift, Dryer_production, Mill_production, Equipement, ExpeditionData, Port_production, Feedback, Performance
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = '__all__'


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Used to display CRO details in the dropdown on the frontend.
    """

    class Meta:
        model = Profile
        fields = '__all__'
        # Note: You can add other fields like phone_number if needed for the UI.


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for the login process.
    It doesn't correspond to a model, but helps validate input and return a token.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
       # Hash the password using set_password()
        # user.set_password(validated_data['password'])
        
        # Save the hashed password to the database
        # user.save()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        print("called")
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

class Dryer_productionSerializer(serializers.ModelSerializer):
     # This is the key change. We explicitly get the shift_number from the related Shift object.
    shift_number = serializers.CharField(source='shift.shift_number', read_only=True)
    class Meta:
        model = Dryer_production
        fields = '__all__'

class Mill_productionSerializer(serializers.ModelSerializer):
     # This is the key change. We explicitly get the shift_number from the related Shift object.
    shift_number = serializers.CharField(source='shift.shift_number', read_only=True)
    class Meta:
        model = Mill_production
        fields = '__all__'

class Port_productionSerializer(serializers.ModelSerializer):
     # This is the key change. We explicitly get the shift_number from the related Shift object.
    shift_number = serializers.CharField(source='shift.shift_number', read_only=True)
    class Meta:
        model = Port_production
        fields = '__all__'

class ExpeditionDataSerializer(serializers.ModelSerializer):
     # This is the key change. We explicitly get the shift_number from the related Shift object.
    shift_number = serializers.CharField(source='shift.shift_number', read_only=True)
    class Meta:
        model = ExpeditionData
        fields = '__all__'
     

class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipement
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'









        