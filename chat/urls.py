from django.urls import path,include

from .views import CreateGroup,GetAddRemoveGroupMember,SendAndGetMessage,LikeOrUnlike

urlpatterns = [
    path('group/', CreateGroup.as_view()),
    path('members/', GetAddRemoveGroupMember.as_view()),
    path('send/', SendAndGetMessage.as_view()),
    path('like/', LikeOrUnlike.as_view())
]