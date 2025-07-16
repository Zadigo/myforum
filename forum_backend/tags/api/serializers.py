from rest_framework import serializers
from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model"""
    
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']

    def validate_name(self, value):
        """
        Validate that the tag name is not empty and does not contain special characters.
        """
        if not value or not value.isalnum():
            raise serializers.ValidationError("Tag name must be alphanumeric and cannot be empty.")
        return value
