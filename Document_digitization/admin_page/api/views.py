from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from admin_page.models import *
from admin_page.api.serializers import *

class  GroupView(viewsets.ModelViewSet):
    queryset = User_Group.objects.all()
    serializer_class = GroupSerializer

class  RoleView(viewsets.ModelViewSet):
    queryset = User_Role.objects.all()
    serializer_class = RoleSerializer

class  UserView(viewsets.ModelViewSet):
    queryset = Plan_User.objects.all()
    serializer_class = UserSerializer

class  FilesView(viewsets.ModelViewSet):
    queryset = Doc_Files.objects.all()
    serializer_class = FilesSerializer

class  AvatarView(viewsets.ModelViewSet):
    queryset = avatar.objects.all()
    serializer_class = AvatarSerializer

class  NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
