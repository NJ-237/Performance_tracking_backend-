from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile
from .models import Shift, Dryer_production, Mill_production, Equipement, ExpeditionData
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


    # Get an existing user
# user = User.objects.get(username='moose')

    # Or create a new user (and its associated profile will be created automatically if you override save() in Profile)
# user = User.objects.create_user(username='new_user', password='password123')

# users_to_update = User.objects.filter(is_active=True) # Example: filter active users

# for user in users_to_update:
#     profile = user
#     profile.bio = f"Updated bio for {user.username}"
#     profile.save

# from django.db import migrations



# class RoleSpecificSerializer(serializers.ModelSerializer):
        # class Meta:
#             model = Shift
#             fields = ['CRO1', 'CRO2', 'Patroller1', 'Patroller2', 'CDQ'] # Fields visible for a specific role


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





class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=100)
    email = serializers.EmailField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)

    def create(self, validated_data):
      with transaction.atomic():
        phone_number = validated_data.pop('phone_number', None)
        service_location = validated_data.pop('service_location', None)
        position = validated_data.pop('position', None)
        employee_id = validated_data.pop('employee_id', None)
        gender = validated_data.pop('gender', None)
        email = validated_data.pop('email', None)
        User.set_password ( validated_data.pop('password', None))
        username = validated_data.pop('username', None)
       
    #  # ... inside your registration view or function
    #     username = requests.post('username')

    #     if User.objects.filter(username=username).exists():
    #         # Handle the error, e.g., return an API response with an error message
    #         return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    # # Proceed with creating the new user
    # # ...

        # user = User.objects.create_user(
        #     username=username,
        #     password=password,
        #     email=email,
            
        # )

        # Profile.objects.create(
        #     # user=user,
        #     phone_number=phone_number,
        #     Service_location=service_location,  
        #     Position=position,                  
        #     Employee_id=employee_id,           
        #     Gender=gender,      
         
           
        # )

        # # if phone_number:
        # #     Profile.objects.create(user=user, phone_number=phone_number)
        # return user

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
    class Meta:
        model = Dryer_production
        fields = '__all__'

class Mill_productionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mill_production
        fields = '__all__'

# class PortDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PortData
#         fields = '__all__'

class ExpeditionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpeditionData
        fields = '__all__'

class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipement
        fields = '__all__'
