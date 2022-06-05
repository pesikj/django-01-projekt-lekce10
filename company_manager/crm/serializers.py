from rest_framework import serializers
from crm.models import Company, Opportunity

class OpportunitySerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    sales_manager = serializers.StringRelatedField()

    class Meta:
        model = Opportunity
        fields = ['company', 'status', 'sales_manager', 'value']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'status', 'identification_number', 'email']
