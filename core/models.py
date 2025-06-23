# backend/core/models.py
from django.db import models
# from django.contrib.auth.models import User # <-- DELETE this line
from django.conf import settings # <-- ADD this line

class Category(models.Model):
    # CHANGE THIS LINE:
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    # ... rest of the model is the same
    class Meta:
        unique_together = ('user', 'name')
        verbose_name_plural = "Categories"
    def __str__(self): return self.name

class Transaction(models.Model):
    # ... (choices are the same)
    TRANSACTION_TYPE_CHOICES = [('INCOME', 'Income'), ('EXPENSE', 'Expense')]
    # CHANGE THIS LINE:
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    # ... rest of the model is the same
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)
    class Meta: ordering = ['-date']
    def __str__(self): return f"{self.type} of {self.amount} on {self.date}"

class Budget(models.Model):
    # CHANGE THIS LINE:
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    # ... rest of the model is the same
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    class Meta: unique_together = ('user', 'category', 'year', 'month')
    def __str__(self): return f"Budget for {self.category.name} in {self.year}-{self.month}: {self.amount}"