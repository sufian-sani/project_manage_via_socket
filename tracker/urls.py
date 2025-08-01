from django.urls import path
from .views import ProjectViewSet, BugViewSet, CommentViewSet


project_list = ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

project_detail = ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

bug_list = BugViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

bug_detail = BugViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'update',
    'delete': 'destroy',
})

bug_list_assigned = BugViewSet.as_view({
    'get': 'assigned_bugs'
})

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'update',
    'delete': 'destroy',
})


urlpatterns = [
    path('', project_list, name='project-list'),
    path('<int:pk>/', project_detail, name='project-detail'),
    path('bugs/', bug_list, name='bug-list'),
    path('bugs/<int:pk>/', bug_detail, name='bug-detail'),
    path('bugs/assigned/', bug_list_assigned, name='assigned-bugs'),
    path('comments/', comment_list, name='comment-list'),
    path('comments/<int:pk>/', comment_detail, name='comment-detail'),
]