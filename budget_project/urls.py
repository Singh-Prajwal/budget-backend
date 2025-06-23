# backend/budget_project/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

# Import our new custom login view
from users.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # App-specific API routes
    path('api/', include('core.urls')),
    path('api/user/', include('users.urls')), # Add the new user urls

    # Authentication routes
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]