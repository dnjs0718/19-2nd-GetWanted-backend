"""getwanted URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework import routers, permissions
from users.views import ApplyView, ApplylistView

schema_view = get_schema_view(
    openapi.Info(
        title="project A title", # 타이틀
        default_version='v1', # 버전
        description="프로젝트 API 문서", # 설명
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mystund@naver.com"),
        license=openapi.License(name=""),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path('users', include('users.urls')),
    path('notifications',include('companies.urls')),
    path('resumes', include('resumes.urls')),
    path('applylist', ApplylistView.as_view()),
    path('apply', ApplyView.as_view())
    ]