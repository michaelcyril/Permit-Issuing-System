from django.urls import path
from .views import *
app_name = 'service_management'

urlpatterns = [
    path('request-get-permit', RequestPermitView.as_view(), name="request_get_permit"),
    path('change-permit-status', ChangePermitStatusView.as_view(), name="request_get_permit"),
    path('change-payment-status', ChangePermitPaymentStatusView.as_view(), name="request_get_permit"),
    
    path('get-all-permit', GetPermitView.as_view(), name="get_all_permit"),
    path('get-permit-information', GetPermitInformation.as_view(), name="get_permit_information"),
]