from django.urls import path
from . import views

urlpatterns = [
    path('gender/list/', views.gender_list, name='gender_list'),
    path('gender/add/', views.add_gender, name='add_gender'),
    path('gender/edit/<int:genderId>/', views.edit_gender, name='edit_gender'),
    path('gender/delete/<int:genderId>/', views.delete_gender, name='delete_gender'),
    path('user/add/', views.add_user, name='add_user'),
    path('user/list/', views.user_list, name='user_list'),
    path('user/delete/<int:userId>/', views.delete_user, name='delete_user'),
    path('user/edit/<int:userId>/', views.edit_user, name='edit_user')
]