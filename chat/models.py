import uuid
from django.contrib.auth.models import User
from django.db import models


class Groups(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, blank=False, null=False, default=uuid.uuid4())
    title = models.CharField(max_length=250, blank=False, null=False)
    member_count = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Member_name')

    class Meta:
        ordering = ['title', ]
        db_table = 'Groups'

    def __str__(self):
        return self.title


class GroupMember(models.Model):
    id = models.UUIDField(primary_key=True, blank=False, null=False, default=uuid.uuid4())
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='group_name')
    user_id = models.ManyToManyField(User, related_name='group_member')

    def __str__(self):
        return self.group_id.title


class Messages(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE)
    message = models.CharField(max_length=500,blank=False, null=False)
    send_time = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)



class Likes(models.Model):

    like_by = models.ForeignKey(User, on_delete=models.CASCADE)
    message_id = models.ForeignKey(Messages, on_delete=models.CASCADE)
    like_time = models.DateTimeField(auto_now_add=True)

