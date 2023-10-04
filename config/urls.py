from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenBlacklistView


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="WinCo API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/",
      contact=openapi.Contact(email="winco@gmail.com"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/v1/auth/',include('authentification.urls')),
    path('api/v2/follwer/', include('follower.urls')),
    path('api/v3/post/', include('post.urls')),
    path('api/v4/msg/', include('message.urls')),
]


# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)