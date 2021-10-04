from decouple import config


from rest_framework.views import exception_handler
from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import generics, permissions, serializers, viewsets, status

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Send_cargo
from .serializers import UserProfileSerializer, User_infSerializer, Nested_send_cargoSerializer, LoginSerializer, ChangePasswordSerializer, Userupdateimage, UserUpdatephone


from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class Sign_Up_Views(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = User_infSerializer


class Send_cagro_View(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'Send_cargo_id'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = Nested_send_cargoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.group == 'driver':
            return Send_cargo.objects.filter(
                Q(status=Send_cargo.REQUESTED) | Q(driver=user)
            )
        if user.group == 'rider':
            return Send_cargo.objects.filter(rider=user)
        return Send_cargo.objects.none()


class Loginview(TokenObtainPairView):
    serializer_class = LoginSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                response = {
                    'status': 400,
                    'code': 400,
                    'message': 'Wrong current password ',
                    'data': []
                }
                return Response(response)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 200,
                'code': 200,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = User_infSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserDetail, self).get_object()


class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    queryset = get_user_model().objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserProfileUpdateView, self).get_object()


class UserProfileUpdatephone(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserUpdatephone

    queryset = get_user_model().objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserProfileUpdatephone, self).get_object()


class UserProfileUpdateimage(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = Userupdateimage

    queryset = get_user_model().objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserProfileUpdateimage, self).get_object()


def outside_view_500_error_handler(request):

    # set status

    status1 = status.HTTP_500_INTERNAL_SERVER_ERROR
    # set body
    body = '<h1>Can not delete this account, because it have link to send cargo trip with other customer. Go back to admin control <a href=/>Home</a> </h1>'.encode(
        'UTF-8')

    # create response
    r = HttpResponse(body, status=status1,)

    # add headers

    return r


def outside_view_x_error_handler(request):

    # set status

    status1 = status.HTTP_400_BAD_REQUEST
    # set body
    body = '<h1>Can not delete this account, because it have link to send cargo trip with other customer. Go back to admin control <a href=/>Home</a> </h1>'.encode(
        'UTF-8')

    # create response
    r = HttpResponse(body, status=status1,)

    # add headers

    return r
