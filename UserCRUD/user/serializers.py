from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from .models import CustomUser, Organization, Address


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'city', 'state', 'country']
        extra_kwargs = {
            'address_line2': {'required': False},
            'state': {'required': False}
        }


class CustomUserGetSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    addresses = AddressSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name', 'email', 'mobile_number', 'organization', 'addresses']


class CustomUserSerializer(serializers.ModelSerializer):
    organization_id = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), source='organization',
                                                         write_only=True)
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'full_name', 'email', 'mobile_number', 'organization_id', 'addresses']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    {
        "username": "user6",
        "full_name": "user6",
        "email": "user6@example.com",
        "mobile_number": "03912861234",
        "organization": {
            "name": "organization_2"
        },
        "addresses": [
            {
                "address_line1": "add1",
                "address_line2": "add2",
                "city": "isb",
                "state": "isb",
                "country": "pakistan"
            }
        ]
    }

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        user = CustomUser.objects.create_user(**validated_data)
        for address_data in addresses_data:
            Address.objects.create(user=user, **address_data)
        return user

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        instance = super().update(instance, validated_data)
        print(addresses_data)
        for address_data in addresses_data:
            Address.objects.create(user=instance, **address_data)

        return instance


class CreateCustomUserSerializer(serializers.ModelSerializer):
    organization_id = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(),
                                                         source='Organization')

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        organization = validated_data.pop('Organization')
        if organization:
            validated_data['organization_id'] = organization.id
            # del validated_data['Organization']
        user = CustomUser.objects.create(**validated_data)
        # user.organization_id = Organization.id
        user.set_password(validated_data['password'])
        print("Before Save")
        print(user)
        user.save()
        print("After Save")
        return user

    # Make addresses field optional
    addresses = AddressSerializer(many=True, read_only=True, required=False)
