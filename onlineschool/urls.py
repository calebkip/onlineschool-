from importlib.resources import path
from django import urls
from django.urls import path
from . import views


urlpatterns=[

    path('login/',views.loginPage,name="login"),
    path('register/',views.registerPage,name="register"),
    path('logout/',views.logoutUser,name="logout"),
    path ('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('profile/<str:pk>/',views.userProfile,name="user_profile"),
    path('createRoom/',views.createRoom,name="createRoom"),
    path('updateRoom/<str:pk>/',views.updateRoom,name="updateRoom"),
    path('deleteRoom/<str:pk>/',views.deleteRoom,name="deleteRoom"),
    path('delete_message/<str:pk>/',views.delete_message,name="delete_message"),
]