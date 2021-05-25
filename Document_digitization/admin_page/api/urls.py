from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('User_Group', views.GroupView)
router.register('User_Role', views.RoleView)
router.register('Plan_User', views.UserView)
router.register('Doc_Files', views.FilesView)
router.register('avatar', views.AvatarView)
router.register('Notification', views.NotificationView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
