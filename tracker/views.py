from django.shortcuts import render
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer

class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class TransactionList(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

class Summary(APIView):
    def get(self, request):
        total_income = Transaction.objects.filter(is_income=True).aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Transaction.objects.filter(is_income=False).aggregate(total=Sum('amount'))['total'] or 0
        savings = total_income - total_expense

        biggest_expense_category = Transaction.objects.filter(is_income=False)\
            .values('category__name')\
            .annotate(total_amount=Sum('amount'))\
            .order_by('-total_amount')\
            .first()

        summary_data = {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "savings": float(savings),
            "biggest_expense_category": biggest_expense_category['category__name'] if biggest_expense_category else "N/A",
        }
        return Response(summary_data)

def dashboard(request):
    return render(request, "tracker/dashboard.html")