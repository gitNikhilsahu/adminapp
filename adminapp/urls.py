from django.urls import path, include
from adminapp import views


urlpatterns = [
    path('', views.home_view, name='homev'),
    path('home/', views.home, name='home'),
    # admin urls
    path('myadmin/', views.myadmin_view, name='myadmin'),
    path('myadmin/users/', views.user_list_view, name='users'),
    path('myadmin/users/<int:id>/', views.update_view, name='update'),
    path('myadmin/users/<int:id>/delete/', views.delete_view, name='delete'),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
]
