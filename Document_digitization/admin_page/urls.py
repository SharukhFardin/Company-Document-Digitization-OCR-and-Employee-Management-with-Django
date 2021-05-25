from django.urls import path
from . import views
#from .views import admin_page, Create_user

urlpatterns = [
    #path('Create_user', Create_user.as_view(), name="Create_user"),
    #path('admin_page', admin_page.as_view(), name="admin_page"),
    path('Create_user', views.Create_user, name="Create_user"),
    path('admin_page', views.admin_page, name="admin_page"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('admin_profile', views.admin_profile, name="admin_profile"),
    path('login',views.login, name="login"),
    path('search_page',views.search_page, name="search_page"),
    path('A_notification',views.A_notification, name="A_notification"),
    path('A_repository',views.A_repository, name="A_repository"),
    # path('change_pass', views.change_pass, name="change_pass"),
]
