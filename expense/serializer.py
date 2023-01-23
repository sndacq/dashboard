from rest_framework import serializers
from .models import Entry, Account, Category


class IDParamSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="entry id")

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = (
            'actions',
            'date',
            'amount',
            'category',
            'account',
            'to_asset_id',
            'description',
        )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'uid',
            'name',
            'is_trans_expense',
            'value',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'uid',
            'pUid',
        )