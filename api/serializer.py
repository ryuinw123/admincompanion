from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import Marker , Event , Image , Comment , ReportEvent , ReportMarker , EventUrl



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True,) #validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    secret = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2','secret')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        secret = attrs["secret"]
        if secret != 'secret':
            raise serializers.ValidationError(
                {"secret": "Invalid secret code."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = '__all__'
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUrl
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='image_id')
    dataURL = serializers.CharField(source='link')
    class Meta:
        model = Image
        fields = ['id','dataURL']

class ImageEventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='image_id')
    dataURL = serializers.CharField(source='link')
    class Meta:
        model = Image
        fields = ['id','dataURL']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReportMarkerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReportMarker
        fields = '__all__'


class ReportEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportEvent
        fields = '__all__'
