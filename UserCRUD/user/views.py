from django.db.models import Q
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser, Organization, Address
from .permissions import IsOwnerOrReadOnly, IsUserOrganization
from .serializers import CustomUserGetSerializer, CustomUserSerializer, CreateCustomUserSerializer, \
    OrganizationSerializer, AddressSerializer


class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class CustomUserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class CustomUsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserGetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(Q(organization=self.request.user.organization)
                                       | Q(id=self.request.user.id))
        return queryset


class CustomUserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserGetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(Q(organization=self.request.user.organization)
                                       | Q(id=self.request.user.id))
        return queryset


class CustomUserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsUserOrganization]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(Q(id=self.request.user.organization.id))
        return queryset


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
