from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework_jwt.settings import api_settings
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializer import MemberSerializer
from django.contrib.auth.models import User
from restconfig.util import jwt_response_payload_handler

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class MemberAPIView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    serializer_class = MemberSerializer
    queryset = User.objects.all()


class MemberDetailAPIView(mixins.DestroyModelMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]
    serializer_class = MemberSerializer
    queryset = User.objects.all()

    # def get_object(self):
    #     userid = self.kwargs["pk"]
    #     print(userid)
    #     return get_object_or_404(User, id=userid)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AuthApiView(APIView):
    permission_classes = [AllowAny]

    # authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        username = data.get('username')
        password = data.get('password')
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return Response(
                {'Detail': 'is Authenticate'})
        user = authenticate(username=username, password=password)
        q = User.objects.filter(
            Q(username__iexact=username) or Q(email__iexact=username)
        ).distinct()
        print(q)
        if q.count() == 1:
            usr_obj = q.first()
            if usr_obj.check_password(password):
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                print(Response)
                return Response(response, status=400)

        return Response({'Detail': 'bad response'}, status=401)
