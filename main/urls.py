from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('login', views.Login, name='login'),
    path('register', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),
    path('rooms', views.Room_List, name='Rooms'),
    path('',views.Home,name='home'),
    path('description', views.Description, name='description'),
    path('book', views.Book,name='book'),
    path('payment', views.Payment, name = 'payment'),
    path('advertise', views.Advertise, name = 'advertise'),
    path('comment', views.Comments, name ='comment'),
    path('adminpage', views.Adminpage, name='landlord'),
    path('verify', views.VerifyRoom, name ='verify'),
]