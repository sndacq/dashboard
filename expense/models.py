import datetime

from django.db import models
from django.utils import timezone

class Account(models.Model):
    account_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.account_name


class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Expense(models.Model):
    class ExpenseType(models.IntegerChoices):
        INCOME = 0
        EXPENSE = 1
        TRANSFER = 3
        SAVINGS = 4

    date = models.DateField('entry date')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    expense_type = models.IntegerField(choices=ExpenseType.choices)

    def __str__(self):
        return self.date.strftime("%m/%d/%Y, %H:%M:%S")