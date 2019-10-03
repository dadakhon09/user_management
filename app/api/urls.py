from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from app.api.users.views import UserRegister, UserLogin, UserLogout, UserUpdate, UserDelete

schema_view = get_swagger_view(title='Documentation')


urlpatterns = [
    path('user/register/', UserRegister.as_view(), name='register'),
    path('user/login/', UserLogin.as_view(), name='login'),
    path('user/logout/', UserLogout.as_view(), name='logout'),
    path('user/<int:user_id>/update/', UserUpdate.as_view(), name='user-update'),
    path('user/<int:user_id>/delete/', UserDelete.as_view(), name='user-delete'),
]
