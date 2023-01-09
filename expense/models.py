from django.db import models

class Account(models.Model):
    uid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    is_trans_expense = models.BooleanField(default=False)
    value = models.BigIntegerField()


class Category(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    pUid = models.CharField(max_length=200)

class Entry(models.Model):
    INCOME = 0
    EXPENSE = 1
    TRANSFER = 3
    SAVINGS = 4
    ACTION_CHOICES = [
        (INCOME, 0),
        (EXPENSE, 1),
        (TRANSFER, 3),
        (SAVINGS, 4),
    ]
    actions = models.CharField(
        max_length=200,
        choices=ACTION_CHOICES,
        default=EXPENSE
    )
    date = models.BigIntegerField()
    amount = models.BigIntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    to_asset_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer_account')
    description = models.CharField(max_length=200)