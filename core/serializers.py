# backend/core/serializers.py
from rest_framework import serializers
from .models import Category, Transaction, Budget
from django.conf import settings

# This serializer is for listing/retrieving detailed budget info
class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_name', 'amount', 'month', 'year']

# This serializer is specifically for creating or updating a budget
class BudgetCreateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True)

    class Meta:
        model = Budget
        fields = ['category_name', 'amount', 'month', 'year']

    def create(self, validated_data):
        user = self.context['request'].user
        category_name = validated_data.pop('category_name')

        # Find or create the category for this user
        category, _ = Category.objects.get_or_create(
            user=user,
            name__iexact=category_name,
            defaults={'name': category_name}
        )

        # "Upsert" logic: Update if exists, otherwise create
        budget, created = Budget.objects.update_or_create(
            user=user,
            category=category,
            month=validated_data['month'],
            year=validated_data['year'],
            defaults={'amount': validated_data.get('amount', 0)}
        )
        return budget

# Serializer for Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# Serializer for Transaction
class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Transaction
        fields = ['id', 'category', 'category_name', 'amount', 'type', 'date', 'description']