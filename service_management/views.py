from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .serializer import *
from .models import *
from user_management.models import User


class RequestPermitView(APIView):
    model = Permit
    get_serializer_class = PermitGetSerializer
    post_serializer_class = PermitPostSerializer
    user_model = User

    def post(self, request):
        data = request.data
        print(data)
        serialized = self.post_serializer_class(data=data)
        # print("ddddddddd")
        
        if serialized.is_valid():
            # print(serialized.is_valid())
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "errors": serialized.errors})

    def get(self, request):
        id = request.GET.get("id")
        try:
            customer = self.user_model.objects.get(id=id)
            queryset = self.model.objects.filter(customer=customer)
            serialized = self.get_serializer_class(instance=queryset, many=True)
            return Response({"error": False, "data": serialized.data})
        except self.user_model.DoesNotExist:
            return Response({"error": True})


class ChangePermitStatusView(APIView):
    model = Permit
    user_model = User

    def post(self, request):
        try:
            now = timezone.now()
            data = request.data
            queryset = self.model.objects.get(id=data['id'])
            if data['status'] == "PERMITED":
                queryset.issued_by = self.user_model.objects.get(id=data['request_user'])
                queryset.issued_at = now
                queryset.status = data['status']
                queryset.save()
                
                return Response({"change": True, "message": "Permit successful"})
            elif data['status'] == "CANCELED":
                queryset.canceled_by =  self.user_model.objects.get(id=data['request_user'])
                queryset.status = data['status']
                queryset.canceled_at = now
                queryset.save()
                return Response({"change": True, "message": "Cancel successful"})
            else:
                return Response({"change": False})
        except self.model.DoesNotExist:
            return Response({"change": True})


# {
#     "id": "nnnnn",
#     "request_user": "bccchcjj"
#     "status": "bccchcjj"
# }


class GetPermitView(APIView):
    model = Permit
    get_serializer_class = PermitGetSerializer
    user_model = User

    def get(self, request):
        querset = self.model.objects.all()
        print("querset")
        
        print(querset)
        serialized = self.get_serializer_class(instance=querset, many=True)
        return Response(serialized.data)


class GetPermitInformation(APIView):
    model = Permit
    get_serializer_class = PermitGetSerializer

    def get(self, request):
        id = request.GET.get("id")
        try:
            queryset = self.model.get(id=id)
            serialized = self.get_serializer_class(instance=queryset, many=False)
            return Response({"errors": True, "data": serialized.data})
        except self.model.DoesNotExist:
            return Response({"errors": False})


