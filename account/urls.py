from django.urls import path
from account.views import MemberAPIView, MemberDetailAPIView, AuthApiView

urlpatterns = [
    path('user/',MemberAPIView.as_view()),
    path('user/<int:pk>',MemberDetailAPIView.as_view()),
    path('user/login', AuthApiView.as_view()),
]