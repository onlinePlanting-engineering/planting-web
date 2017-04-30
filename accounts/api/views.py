from django.contrib.auth import get_user_model, authenticate, login, logout

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.generics import (
CreateAPIView,
ListAPIView,
)
from rest_framework.permissions import (
AllowAny,
IsAdminUser,
IsAuthenticated,
IsAuthenticatedOrReadOnly
)

User = get_user_model()

from .serializers import (
UserCreateSerializer,
UserLoginSerializer,
UserListSerializer,
)

class UserListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    queryset = User.objects.all()

    def get(self, request, format=None):
        logout(request)
        return Response(status=HTTP_200_OK)