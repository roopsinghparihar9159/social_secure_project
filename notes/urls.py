from django.urls import path
from notes import views


urlpatterns=[
    path('',views.index,name='Home'),
    path('edit_note/',views.edit_note,name='EditNote'),
    path('delete_note/',views.delete_note,name='DeleteNote'),
    path('signup/',views.signup,name='Signup'),
    path('login/',views.UserLogin,name='Login'),
    path('logout/',views.UserLogout,name='Logout'),
]