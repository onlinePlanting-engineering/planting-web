from farm.models import Farm, FarmImage
from rest_framework import serializers
from accounts.api.serializers import (
    UserSerializer,
    UserFilteredPrimaryKeyRelatedField
)

class FarmSerializer(serializers.ModelSerializer):
    images = serializers.HyperlinkedRelatedField(many=True, view_name='farmimage-detail', read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    notice = serializers.HyperlinkedIdentityField(view_name='farm-notice', format='html')
    content = serializers.HyperlinkedIdentityField(view_name='farm-content', format='html')

    class Meta:
        model = Farm
        fields = ('url', 'id', 'name', 'owner', 'price', 'subject',
                  'is_delete', 'notice', 'content', 'images')

class FarmImageSerializer(serializers.ModelSerializer):
    # Create a custom method field, that list farms belong to current user
    farm = UserFilteredPrimaryKeyRelatedField(queryset=Farm.objects, source='farm.name')

    class Meta:
        model = FarmImage
        fields = ('id', 'url', 'farm', 'image', 'flags', 'is_delete')