from django.contrib.auth import get_user_model, logout

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_404_NOT_FOUND
)
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    AllowAny,
)

User = get_user_model()

from .serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserSerializer,
)
from accounts.models import Profile

class UserListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class UserLogoutAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        logout(request)
        return Response(status=HTTP_200_OK)

@api_view(['PUT'])
@permission_classes((AllowAny, ))
def reset_password(request):
    if request.method != 'PUT':
        return Response(data={
            'detail':'please use PUT http method',
            'status_code': HTTP_405_METHOD_NOT_ALLOWED
        })

    user_obj = None

    username = request.data.get('username', None)
    password = request.data.get('password', None)

    if username:
        qs = User.objects.filter(username=username)
        if qs.exists and qs.count() == 1:
            user_obj = qs.first()

    if not user_obj:
        return Response(data={
            'detail':'phone number not found',
            'status_code':HTTP_404_NOT_FOUND
        }, status=HTTP_404_NOT_FOUND)

    if not password:
        return Response(data={
            'detail': 'invalid password',
            'status_code': HTTP_400_BAD_REQUEST
        }, status=HTTP_400_BAD_REQUEST)

    user_obj.set_password(password)
    user_obj.save()
    return Response(data={
        'detail': 'password update succeed',
        'status_code': HTTP_200_OK
    }, status=HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer