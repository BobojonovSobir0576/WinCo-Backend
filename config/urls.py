from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi





urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path('docs/', TemplateView.as_view(
        template_name='doc.html',
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),



    path('api/auth/',include('authentification.urls')),
    path('api/follwer/', include('follower.urls')),
    path('api/post/', include('post.urls')),
    path('api/msg/', include('message.urls')),
]


# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)