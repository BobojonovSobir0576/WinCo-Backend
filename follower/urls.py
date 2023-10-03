from django.urls import path
from follower import views

urlpatterns = [
    path('follower/', views.GetFollorsView.as_view()),
]