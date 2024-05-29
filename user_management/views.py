from django.db.models import QuerySet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import *
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            email = data['email']
            user = User.objects.filter(email=email)
            if user:
                message = {'save': False, 'message': 'username or email already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"save": True})
        return Response({'save': False, 'message': serializer.errors})

    @staticmethod
    def get(request):
        users  = User.objects.all()
        return Response(UserGetSerializer(instance=users, many=True).data)
# {
# "username":"mike",
# "email":"mike@gmail.com",
# "phone":"0693331836",
# "firstname":"Michael",
# "lastname":"Cyril",
# "usertype":"PERMIT_OFFICER"
# }


class LoginView(APIView):
    permission_classes = [AllowAny]
    model = User

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        print(request.data)
        
        print(email)
        print(password)
        
        print(user)
        if user is not None:
            login(request, user)
            user_id = User.objects.get(email=email)
            user_info = UserGetSerializer(instance=user_id, many=False).data
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'login': True,
                'token': token.key,
                'user': user_info
            }
            return Response(response)
        if user is None:
            
            response = {
                'login': False,
                'msg': 'User doesnot exist',
                # 'msg':user
            }
            return Response(response)
        else:
            response = {
                'login': False,
                'msg': 'Invalid username or password',
            }

            return Response(response)

# {
# "email":"john@gmail.com",
# "password":"123"
# }


class UserInformation(APIView):

    @staticmethod
    def get(request, query_type):
        if query_type == 'single':
            try:
                user_id = request.GET.get('user_id')
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User Does Not Exist'})
            return Response(UserSerializer(instance=user, many=False).data)

        elif query_type == 'all':
            queryset = User.objects.all()
            print (f"queryset: {queryset}")
            return Response(UserGetSerializer(instance=queryset, many=True).data)

        else:
            return Response({'message': 'Wrong Request!'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        print(request.data)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.', 'success': True}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

