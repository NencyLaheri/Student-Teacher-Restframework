
from rest_framework.views import APIView
from .models import ApplicationModel, CustomUser
from .serializers import ApplicationDetailSerializer,UserSerializers,Applicationserializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
def api_root(request,foramt=None):
    return Response({'Registration':reverse('reg',request=request),'Login':reverse('login',request=request)})


class RegistrationView(generics.CreateAPIView):

    queryset=CustomUser.objects.all()
    serializer_class=UserSerializers
   

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
   
    def post(self,request):

        email=request.data['email']
        password=request.data['password']

        try:
            
            user=CustomUser.objects.get(email=email)
           
            if check_password(password,user.password):

                login(request,user)
                u=CustomUser.objects.get(email=user)
                auth_data=get_tokens_for_user(user)
                serializer=UserSerializers(u)
                data={'email':serializer.data['email'],'role':serializer.data['role']}
                return Response({'data':data,'Token':auth_data})   

            else:

                return Response({'message':'incorrect password'})

        except:

            return Response({'message':'user not found'})
    


class DashboardView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        
        s=get_object_or_404(CustomUser,id=id)
        if s.role=='student':
            a=ApplicationModel.objects.filter(customer_id=id)
            serializer=ApplicationDetailSerializer(a,many=True)
            message=('welcome Student '+s.first_name+' '+s.last_name)
            data={'Message':message,'applications':serializer.data}
            return Response(data)
        if s.role=='faculty':
            a=ApplicationModel.objects.all()
            serializer=ApplicationDetailSerializer(a,many=True)
            message=('welcome Faculty '+s.first_name+' '+s.last_name)
            data={'Message':message,'applications':serializer.data}
            return Response(data)        

    def post(self,request,id):
        request.user
        s=get_object_or_404(CustomUser,id=id)
        if s.role=='student':
            serializer=Applicationserializers(data=request.data)
            if serializer.is_valid():
                serializer.save(customer_id=id)
                return Response(serializer.data)
            return Response(serializer.errors)
        if s.role=='faculty':
            return Response({'Error':'Faculty Can Not send Application'})


    def patch(self,request,id):
        s=get_object_or_404(CustomUser,id=id)
        if s.role=='faculty':
            app_id=request.data['app_id']
            ua=get_object_or_404(ApplicationModel,app_id=app_id)
            serializer=ApplicationDetailSerializer(ua,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
       
        if s.role=='student':
            return Response({'Error':'Student Can Not update status'})



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh = request.data["refresh"]
            token = RefreshToken(refresh)
            token.blacklist()

            return Response({"message":'logout successfully'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'message':'Token is invalid or expired'},status.HTTP_400_BAD_REQUEST)