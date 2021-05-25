from django.urls import path
from . import views

urlpatterns = [
    path('e_page', views.e_page, name="e_page"),
    path('e_files', views.e_files, name="e_files"),
    path('pdf_view', views.pdf_view, name="pdf_view"),
    path('E_notification', views.E_notification, name="E_notification"),

]
