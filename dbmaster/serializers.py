from rest_framework import serializers
from dbmaster.models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    vehicle_no = serializers.StringRelatedField(read_only=True)
    trailer_no = serializers.StringRelatedField(read_only=True)
    bp_name = serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Ticket
        fields =['vehicle_no','trailer_no','bp_name','cancelled','created','modified','has_order','has_order_time','loaded','loaded_time',]

