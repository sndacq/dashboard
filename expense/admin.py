from django.contrib import admin
from .models import Expense, Account, Category

admin.site.register(Expense)
admin.site.register(Account)
admin.site.register(Category)
