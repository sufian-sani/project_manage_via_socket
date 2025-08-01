from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Bug, Comment
from .serializers import ProjectSerializer, BugSerializer, CommentSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import action

class ProjectViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)  # Always assign to the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)

        # ✅ Ensure the request user owns this project
        if project.owner != request.user:
            return Response({'detail': 'Permission denied. You do not own this project.'},
                            status=status.HTTP_403_FORBIDDEN)

        # ⚙️ Only update with request data and reassign owner if needed
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)  # guarantees owner is request.user
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)

        # 🔐 Check if the request user is the owner
        if project.owner != request.user:
            return Response({'detail': 'Permission denied. You cannot delete this project.'},
                            status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response({'message': f'Project {pk} deleted successfully'},
                        status=status.HTTP_204_NO_CONTENT)

class BugViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Bug.objects.filter(is_deleted=False)
        status_filter = request.query_params.get('status')
        project_id = request.query_params.get('project')

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        serializer = BugSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BugSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        bug = get_object_or_404(Bug, pk=pk, is_deleted=False)
        serializer = BugSerializer(bug)
        return Response(serializer.data)

    def update(self, request, pk=None):
        bug = get_object_or_404(Bug, pk=pk)
        if bug.created_by != request.user:
            return Response({'detail': 'Permission denied. You cannot update this bug.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = BugSerializer(bug, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        bug = get_object_or_404(Bug, pk=pk)
        if bug.created_by != request.user:
            return Response({'detail': 'Permission denied. You cannot delete this bug.'},
                            status=status.HTTP_403_FORBIDDEN)

        bug.is_deleted = True
        bug.save()
        return Response({'message': f'Bug {pk} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], url_path='assigned')
    def assigned_bugs(self, request):
        user = request.user
        bugs = Bug.objects.filter(assigned_to=user, is_deleted=False)
        serializer = BugSerializer(bugs, many=True)
        return Response(serializer.data)
    
class CommentViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(commenter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.commenter != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(commenter=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.commenter != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({'message': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)