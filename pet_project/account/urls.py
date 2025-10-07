from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import (
    RegisterUser,
    login_user,
    logout_user,
    profile_settings,
)


urlpatterns = [
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile_settings/', profile_settings, name='profile_change'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT
]

# для DEBUG = True
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from rest_framework_simplejwt.serializers import TokenObtainSerializer