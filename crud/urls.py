from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),  
    path('gender/list/', views.gender_list, name='gender_list'),
    path('gender/add/', views.add_gender, name='add_gender'),
    path('gender/edit/<int:genderId>/', views.edit_gender, name='edit_gender'),
    path('gender/delete/<int:gender_id>/', views.delete_gender, name='delete_gender'),
    path('user/list/', views.user_list, name='user_list'),
    path('user/add/', views.add_user, name='add_user'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),  
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user/change_password/<int:user_id>/', views.change_password, name='change_password'),]