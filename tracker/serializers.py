from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Bug, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner']
        
class BugSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )
    created_by = serializers.ReadOnlyField(
        source='created_by.username'
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all()
    )

    class Meta:
        model = Bug
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assigned_to',
            'project',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        
        
class CommentSerializer(serializers.ModelSerializer):
    commenter = serializers.ReadOnlyField(source='commenter.username')
    bug = serializers.PrimaryKeyRelatedField(queryset=Bug.objects.filter(is_deleted=False))

    class Meta:
        model = Comment
        fields = ['id', 'bug', 'commenter', 'message', 'created_at', 'updated_at']
        read_only_fields = ['commenter', 'created_at', 'updated_at']