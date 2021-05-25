from django.urls import path
from . import views
#from .views import admin_page, Create_user

urlpatterns = [
    #path('Create_user', Create_user.as_view(), name="Create_user"),
    #path('admin_page', admin_page.as_view(), name="admin_page"),
    #path('Create_user', views.Create_user, name="Create_user"),
    path('manager_page', views.manager_page, name="manager_page"),
    path('manager_profile', views.manager_profile, name="manager_profile"),
    path('c_group', views.c_group, name="c_group"),
    path('pdf_view', views.pdf_view, name="pdf_view"),
    path('M_notification', views.M_notification, name="M_notification"),

    #path('logout_user', views.logout_user, name="logout_user"),
    #path('admin_profile', views.admin_profile, name="admin_profile"),
]
