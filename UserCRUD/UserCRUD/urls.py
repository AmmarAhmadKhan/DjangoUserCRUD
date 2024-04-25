"""
URL configuration for UserCRUD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import (CustomUsersListView, CustomUserCreateView, CustomUserDetailView,
                        OrganizationViewSet, AddressViewSet, CustomUserDeleteView,
                        CustomUserUpdateView)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()
router.register(r'organization', OrganizationViewSet)
router.register(r'address', AddressViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="My User CRUD APIs",
        default_version='v1',
        description="APIs for User CRUD Operations",
        contact=openapi.Contact(email="ammar0697@gmail.com")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('users/', CustomUserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('users/all/', CustomUsersListView.as_view(), name='all-users-list'),
    path('users/delete/<int:pk>/', CustomUserDeleteView.as_view(), name='user-delete'),
    path('users/update/<int:pk>/', CustomUserUpdateView.as_view(), name='user-update'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
