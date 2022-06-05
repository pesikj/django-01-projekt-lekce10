import django_tables2 as tables
from crm.models import Opportunity
from django_tables2.utils import A

class OpportunityTable(tables.Table):
    company = tables.LinkColumn("opportunity_update", args=[A("pk")],
                                attrs={"a": {"class": "cell-with-link"}})

    class Meta:
        model = Opportunity
        fields = ("company", "sales_manager", "status", "value", "updated_on")
