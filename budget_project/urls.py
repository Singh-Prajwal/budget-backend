from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Import our new custom login view
from users.views import MyTokenObtainPairView

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint"""
    return JsonResponse({
        'message': 'Budget Tracker API',
        'version': '2.0',
        'endpoints': {
            'auth': '/api/token/',
            'refresh': '/api/token/refresh/',
            'register': '/api/user/register/',
            'categories': '/api/categories/',
            'transactions': '/api/transactions/',
            'budgets': '/api/budgets/',
            'summary': '/api/summary/',
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API root
    path('api/', api_root, name='api-root'),
    path('', api_root, name='root'),
    
    # App-specific API routes
    path('api/', include('core.urls')),
    path('api/user/', include('users.urls')),

    # Authentication routes
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]