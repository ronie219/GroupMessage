from rest_framework import serializers
from .models import Groups, GroupMember,Messages


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = [
            'id',
            'title',
            'member_count'
        ]


class GroupMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMember
        fields = [
            'group_id',
            'user_id'
        ]
        # depth = 1


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'

