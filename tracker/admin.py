from django.contrib import admin
from .models import Transaction, Category

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'category', 'is_income', 'payment_method')
    list_filter = ('date', 'category', 'is_income', 'payment_method')
    search_fields = ('description', 'notes')
    list_per_page = 25

# Register your models with the admin site
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)