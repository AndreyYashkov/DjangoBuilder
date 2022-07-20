from rest_framework import viewsets, status, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, RegisterSerializer


class UserViewSet(
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet,
    ):
    queryset = User.objects
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        "create": [permissions.AllowAny,],
    }

    def get_permissions(self):
        if self.action in self.permission_classes_by_action:
            permissions = self.permission_classes_by_action[self.action]
        else:
            permissions = self.permission_classes
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action == "create":
            return RegisterSerializer
        return self.serializer_class

    @action(methods=["GET", "PUT", "DELETE"], detail=False)
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serialized_user = self.get_serializer(instance=user)
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        if request.method == "PUT":
            serialized_user = self.get_serializer(instance=user, data=request.data, partial=True)
            serialized_user.is_valid(raise_exception=True)
            serialized_user.save()
            return Response(serialized_user.data, status=status.HTTP_202_ACCEPTED)
        if request.method == "DELETE":
            user.is_active = False
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
