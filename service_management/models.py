from django.db import models
from user_management.models import User
import uuid

class Permit(models.Model):
    STATUS = (
        ("PENDING", "Pending"),
        ("PERMITED", "Permited"),
        ("CANCELED", "Canceled"),
    )
    PERMIT_TYPE = (
        ("TRANSFER", "Transfer"),
        ("SELLING", "Selling"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="permit_issued_by",null=True)
    issued_at = models.DateTimeField(null=True)
    canceled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="permit_canceled_by",null=True)
    canceled_at = models.DateTimeField(null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_request_permit")
    livestock_number = models.IntegerField()
    permit_number = models.CharField(max_length=250, null=True, blank=True)
    permit_typec = models.CharField(max_length=250, choices=PERMIT_TYPE, null=True, blank=True)
    status = models.CharField(max_length=250, choices=STATUS,default="PENDING" ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f''

    class Meta:
        db_table = 'permit_table'
