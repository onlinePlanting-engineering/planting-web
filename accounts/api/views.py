from django.contrib.auth import get_user_model, logout
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_404_NOT_FOUND
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from accounts.permissions import IsOwnerOrReadOnly

User = get_user_model()

from .serializers import (
    UserCreateSerializer,
    UserSerializer,
    ChangeUsernameSerializer
)

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Create a model instance.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(data={
                'data': serializer.data,
                'status_code': status.HTTP_201_CREATED
            }, status=status.HTTP_201_CREATED, headers=headers)

        return Response(data={
            'data': serializer.errors,
            'status_code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)



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

    if not password or len(password) < 6:
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

@api_view(['GET'])
@permission_classes((IsOwnerOrReadOnly, IsAuthenticated))
def get_current_user_info(request):

    user_info = request.user

    serializer = UserSerializer(user_info)

    return Response(data={
        'status_code' : HTTP_200_OK,
        'data' : serializer.data
    }, status=HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route()
    def list_users(self, request):
        users = User.objects.all().order_by('-id')
        serializer = self.get_serializer(users, many=True)
        return Response({
            'data': serializer.data,
            'status_code': HTTP_200_OK
        }, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'status_code': HTTP_200_OK
        }, status=HTTP_200_OK)

    @detail_route()
    def get_user_info(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response({
            'data': serializer.data,
            'status_code': HTTP_200_OK
        }, status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'data': serializer.data,
                'status_code': HTTP_200_OK
            }, status=HTTP_200_OK)
        return Response(data={
            'detail': serializer.errors,
            'status_code': HTTP_400_BAD_REQUEST
        }, status=HTTP_400_BAD_REQUEST)


class ChangeUsernameView(UpdateAPIView):
    """
    Endpoint for changing phone number
    """
    serializer_class = ChangeUsernameSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_uid = self.object.id
        current_username = self.object.username

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # The username that need be updated to
            new_username = serializer.data['username']

            # Check if the current user name is the same as the new one
            if new_username == current_username:
                return Response(data={
                    'detail': 'Please enter a new phone number',
                    'status_code': HTTP_400_BAD_REQUEST
                }, status=HTTP_400_BAD_REQUEST)

            # check if the new username has been registered
            qs = User.objects.filter(username=new_username)
            if qs.exists():
                return Response(data={
                    'detail': 'The phone number has been registered',
                    'status_code': HTTP_400_BAD_REQUEST
                }, status=HTTP_400_BAD_REQUEST)

            self.object.username = new_username
            self.object.save()

            return Response(data={
                'data':'Success',
                'status_code': HTTP_200_OK
            }, status=HTTP_200_OK)

        return Response(data={
            'detail': serializer.errors,
            'status_code': HTTP_400_BAD_REQUEST
        }, status=HTTP_400_BAD_REQUEST)