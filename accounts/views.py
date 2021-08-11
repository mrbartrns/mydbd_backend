from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *


# from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


# Create your views here.
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ValidateSimpleJwtTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # if authenticated, simple-jwt returns request.user object
            serializer = UserSerializer(request.user).data
            return Response({'user': serializer}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

# obtain-token-view generates token when user attempts logging in
# class UserLoginView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         serializer = LoginUserSerializer(data=request.data)
#         if serializer.is_valid():
#             pass
#             # generate token

# class ValidateJwtTokenView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         try:
#             token = request.META.get('HTTP_AUTHORIZATION', ' ')
#             print(token)
#             data = {'token': token.split(" ")[1]}
#             validated_data = VerifyJSONWebTokenSerializer().validate(data)
#             user = validated_data['user']
#             user = UserSerializer(user)
#         except Exception as e:
#             return Response(e)
#
#         return Response(user.data, status=status.HTTP_200_OK)


# EXAMPLE
# @api_view(['GET'])
# def validate_jwt_token(request):
#     try:
#         token = request.META.get('HTTP_AUTHORIZATION', ' ')
#         data = {'token': token.split(" ")[1]}
#         validated_data = VerifyJSONWebTokenSerializer().validate(data)
#         user = validated_data['user']
#         user = UserSerializer(user)
#     except Exception as e:
#         return Response(e)
#
#     return Response(user.data, status=status.HTTP_200_OK)
