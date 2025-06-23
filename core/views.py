# backend/core/views.py
from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime
from rest_framework.filters import SearchFilter

from .models import Category, Transaction, Budget
from .serializers import (
    CategorySerializer, 
    TransactionSerializer, 
    BudgetSerializer, 
    BudgetCreateSerializer
)

# --- THE CORRECTED AND FINAL BaseViewSet ---
class BaseViewSet(viewsets.ModelViewSet):
    """
    A base viewset that automatically handles user-specific data.
    - Filters querysets to only the logged-in user's data.
    - Automatically assigns the logged-in user when creating a new object.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # This will work for any model with a 'user' foreign key.
        # It correctly uses the `self.queryset` attribute defined in the child class.
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        This is the crucial fix. This method is inherited by TransactionViewSet.
        It passes the logged-in user directly to the serializer's save method,
        which then includes it in the `create` call.
        e.g., Transaction.objects.create(user=self.request.user, ...other_data)
        """
        serializer.save(user=self.request.user)


# --- Category ViewSet (Inherits the working BaseViewSet) ---
class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# --- Transaction ViewSet (Inherits the working BaseViewSet) ---
class TransactionViewSet(BaseViewSet):
    queryset = Transaction.objects.all().select_related('category')
    serializer_class = TransactionSerializer
    filter_backends = [SearchFilter]
    search_fields = ['description', 'category__name']

    def get_queryset(self):
        # We start with the user-filtered queryset from the base class
        queryset = super().get_queryset() 
        # Then we apply additional filters
        transaction_type = self.request.query_params.get('type')
        if transaction_type in ['INCOME', 'EXPENSE']:
            queryset = queryset.filter(type=transaction_type)
        return queryset


# --- Budget ViewSet (Needs special handling, so it overrides create) ---
class BudgetViewSet(BaseViewSet):
    queryset = Budget.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BudgetCreateSerializer
        return BudgetSerializer
    
    # This create method handles the "database is locked" error for bulk budget saves.
    def create(self, request, *args, **kwargs):
        # Check if the incoming data is a list (for bulk creation)
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Use a single database transaction for the whole operation
            with transaction.atomic():
                # The serializer's create method needs the 'request' in its context
                # to get the user.
                serializer.save(context={'request': request})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
# --- Financial Summary View (Unaffected, but included for completeness) ---
class FinancialSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # ... (logic remains the same)
        today = datetime.today()
        month = int(request.query_params.get('month', today.month))
        year = int(request.query_params.get('year', today.year))
        user = request.user
        total_income = Transaction.objects.filter(user=user, type='INCOME', date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = Transaction.objects.filter(user=user, type='EXPENSE', date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
        expenses_by_category = Transaction.objects.filter(user=user, type='EXPENSE', date__year=year, date__month=month).values('category__name').annotate(total=Sum('amount')).order_by('-total')
        budgets = Budget.objects.filter(user=user, year=year, month=month)
        budget_vs_actual = []
        for budget in budgets:
            actual = Transaction.objects.filter(user=user, type='EXPENSE', date__year=year, date__month=month, category=budget.category).aggregate(total=Sum('amount'))['total'] or 0
            budget_vs_actual.append({ 'category_name': budget.category.name, 'budgeted_amount': budget.amount, 'actual_amount': actual, 'difference': budget.amount - actual })
        summary = { 'total_income': total_income, 'total_expenses': total_expenses, 'balance': total_income - total_expenses, 'expenses_by_category': list(expenses_by_category), 'budget_vs_actual': budget_vs_actual }
        return Response(summary)