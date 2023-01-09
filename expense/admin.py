from django.contrib import admin
from .models import Entry, Account, Category

admin.site.register(Entry)
admin.site.register(Account)
admin.site.register(Category)