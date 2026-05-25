from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Association, UserProfile
from .serializers import AssociationSerializer, UserProfileSerializer, UserSerializer


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AssociationListView(generics.ListAPIView):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_view(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "username and password required"}, status=400)
    user = User.objects.create_user(username=username, email=email, password=password)
    UserProfile.objects.create(user=user)
    return Response(UserSerializer(user).data, status=201)
