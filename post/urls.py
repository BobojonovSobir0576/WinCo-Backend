from django.urls import path
from . import views

urlpatterns = [
    path('post_list/', views.PostView.as_view()),
    path('post_list/<int:id>/', views.PostDetailView.as_view()),
    path('post_like/<int:id>/', views.PostLikeView.as_view()),
    path('post_unlike/<int:id>/', views.PostUnlikeView.as_view()),

]