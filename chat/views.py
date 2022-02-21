from django.contrib.auth.models import User
from rest_framework import views, generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response

from .models import Groups, GroupMember, Messages, Likes
from .serializer import GroupSerializer, GroupMemberSerializer, MessageSerializer


class CreateGroup(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        title = request.data['title']
        create_by = request.user

        obj = Groups.objects.create(title=title, created_by=create_by)
        res = GroupSerializer(obj)
        return Response(res.data, status=201)

    def get(self, request, *args, **kwargs):
        grp = Groups.objects.all()
        res = GroupSerializer(grp, many=True)
        return Response(res.data, status=200)


class GetAddRemoveGroupMember(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        grp_id = request.data['group_id']
        usr_id = request.data['user_id']
        if grp_id and usr_id:
            grp = get_object_or_404(Groups, id=grp_id)
            usr = get_object_or_404(User, id=usr_id)

            qs = GroupMember.objects.filter(group_id=grp_id, user_id=usr_id)

            if qs.exists():
                return Response({'error': 'user already exist for this group'}, status=200)
            obj = GroupMember.objects.create(group_id=grp)
            obj.user_id.set([usr, ])
            grp.member_count += 1
            grp.save()
            res = GroupMemberSerializer(obj)
            return Response(res.data, status=201)
        return Response({'error': 'bad request'}, status=404)

    def delete(self, request):
        grp_id = request.data['group_id']
        usr_id = request.data['user_id']
        if grp_id and usr_id:
            qs = GroupMember.objects.filter(group_id=grp_id, user_id=usr_id)
            if not qs.exists():
                return Response({'error': 'No User Found'}, status=200)
            qs[0].delete()
            grp = get_object_or_404(Groups, id=grp_id)
            grp.member_count -= 1
            grp.save()
            return Response({}, status=204)
        return Response({'error': 'bad request'}, status=404)

    def get(self, request):
        grp_id = request.data['group_id']
        if grp_id:
            qs = GroupMember.objects.filter(group_id=grp_id)
            print(qs)
            res = GroupMemberSerializer(qs, many=True)
            return Response(res.data, status=200)
        return Response({'error': 'bad request'}, status=404)


class SendAndGetMessage(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        grp_id = request.data['group_id']
        message = request.data['message']
        if grp_id and message:
            grp_obj = get_object_or_404(Groups, id=grp_id)
            qs = GroupMember.objects.filter(group_id=grp_obj, user_id=request.user)
            if qs.exists:
                msg = Messages.objects.create(group_id=grp_obj, message=message, sender=request.user)
                res = MessageSerializer(msg)
                return Response(res.data, status=201)
            return Response({'error': 'not a member of the group'}, status=404)
        return Response({'error': 'bad request'}, status=404)

    def get(self, request, *args, **kwargs):
        grp_id = request.data['group_id']
        if grp_id:
            grp_obj = get_object_or_404(Groups, id=grp_id)
            qs = Messages.objects.filter(group_id=grp_obj)
            res = MessageSerializer(qs, many=True)
            return Response(res.data, status=200)
        return Response({'error': 'bad request'}, status=404)


class LikeOrUnlike(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        message_id = request.data['message_id']
        if message_id:
            msg_obj = get_object_or_404(Messages, id=message_id)
            lk = Likes.objects.filter(like_by=request.user, message_id=msg_obj)
            if len(lk) > 0:
                lk[0].delete()
                msg_obj.like_count -= 1
                msg_obj.save()
                return Response({'msg': "Unliked"})
            else:
                Likes.objects.create(like_by=request.user, message_id=msg_obj)
                msg_obj.like_count += 1
                msg_obj.save()
                return Response({'msg': "Liked"})
        return Response({'error': 'bad request'}, status=404)
