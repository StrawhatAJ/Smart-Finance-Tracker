from django.urls import path
from .views import CategoryList, TransactionList, Summary, dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('api/categories/', CategoryList.as_view(), name='category-list'),
    path('api/transactions/', TransactionList.as_view(), name='transaction-list'),
    path('api/transactions/<int:pk>/', TransactionList.as_view(), name='transaction-delete'),
    path('api/summary/', Summary.as_view(), name='summary'),
]
