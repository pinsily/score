from django.urls import path

from system import views

urlpatterns = [
    path('api/login/', views.user_login),
    path('api/logout/', views.user_logout),
    path('api/register/', views.user_register),
    path('api/module_list/', views.module_list),
    path('api/professor_list/', views.professor_list),
    path('api/rating/', views.rating),
    path('api/view/', views.rating_view),
    path('api/average/', views.average),
]
