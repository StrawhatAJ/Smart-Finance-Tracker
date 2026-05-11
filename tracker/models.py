from django.db import models
from django.utils import timezone

EXPENSE_KEYWORDS = {
    "Groceries": ["market", "grocery", "e-commerce"],
    "Restaurants": ["restaurant", "cafe", "bar", "takeaway", "delivery"],
    "Transportation": ["auto", "uber", "ola", "rapido", "taxi", "bus", "metro", "fuel", "gas"],
    "Bills & Utilities": ["electricity", "internet", "water", "phone", "gas bill", "utility"],
    "Shopping": ["amazon", "flipkart", "myntra", "mall", "clothing", "electronics"],
    "Health & Wellness": ["pharmacy", "doctor", "hospital", "gym", "fitness"],
    "Entertainment": ["movie", "netflix", "primevideo", "spotify", "tickets", "district", "bookmyshow"],
    "Travel": ["flight", "hotel", "train"],
}

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    PAYMENT_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('UPI', 'UPI'),
        ('Other', 'Other'),
    ]

    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_income = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="UPI")
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.category and not self.is_income and self.description:
            desc_lower = self.description.lower()
            for cat_name, words in EXPENSE_KEYWORDS.items():
                if any(word in desc_lower for word in words):
                    category_obj, created = Category.objects.get_or_create(name=cat_name)
                    self.category = category_obj
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        type_str = 'Income' if self.is_income else 'Expense'
        category_name = self.category.name if self.category else 'Uncategorized'
        return f"{self.date} | {category_name}: ₹{self.amount} ({type_str})"
