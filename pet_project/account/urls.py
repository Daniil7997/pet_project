from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import (RegisterUser, CreateUser, login_user,
                           logout_user, my_profile, user_list, ProfileRUD
                           )


urlpatterns = [
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('my_profile/', my_profile, name='my_profile'),

    path('api/v1/user_list/', user_list, name='user_list'),
    path('api/v1/create_user/', CreateUser.as_view(), name='user_list'),
    path('api/v1/profile/<int:pk>', ProfileRUD.as_view(), name='profile_rud'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT
]
