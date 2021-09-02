from django.urls import path, include
from rest_framework.decorators import api_view
from .views import RoomList, BookingList
from rest_framework.routers import DefaultRouter
from hotel import views
from .views import RegisterView, LoginView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('room_list/', views.RoomList)
# router.register(r'room_list/', RoomList, basename='RoomList')
router.register('booking', views.BookingList)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),

    # path('room/', views.room_list, name='room_list')
]
