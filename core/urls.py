# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TransactionViewSet, BudgetViewSet, FinancialSummaryView

# The router automatically creates the URLs for our ViewSets (list, create, detail, update, delete)
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', FinancialSummaryView.as_view(), name='financial-summary'),
]