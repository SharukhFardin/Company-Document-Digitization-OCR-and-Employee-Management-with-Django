from rest_framework import serializers
from admin_page.models import *


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Group
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Role
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan_User
        fields = "__all__"

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc_Files
        fields = "__all__"

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = avatar
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
