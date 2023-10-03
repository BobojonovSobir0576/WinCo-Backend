from django.urls import path
from . import views


urlpatterns = [
    path('msg_list/', views.MessageListView.as_view()),
    path('msg_create/<int:id>/', views.CreateMsg.as_view()),
    path('msg_details/<int:id>/', views.MessageUserDetailView.as_view()),
    path('msg_delete/<int:id>/', views.MessageReadDeatilView.as_view()),

]