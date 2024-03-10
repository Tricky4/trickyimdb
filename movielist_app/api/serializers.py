from rest_framework import serializers
from movielist_app.models import (WatchList, StreamPlatform, Review)

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('watchlist',)

class WatchlistSerializer(serializers.ModelSerializer):
    # len_title = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')
    
    class Meta:
        model = WatchList
        fields = '__all__'
        # fields = ['id', 'name', 'description']
        # exclude = ['name']
        
    # def get_len_title(self, object):
    #     return len(object.title)
        
    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError("Title and Storyline should be different!")
        else:
            return data
    
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Title is too short!")
        else:
            return value
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchlistSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be different!")
#         else:
#             return data
    
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value