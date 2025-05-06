from .models import Movie
from rest_framework import serializers

# Serializer to convert Movie objects to/from JSON
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
