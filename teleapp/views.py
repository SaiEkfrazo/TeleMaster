from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

CustomUser = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create a record in the GlobalNumbers table and associate it with the user
            name = serializer.validated_data['name']
            phone_number = serializer.validated_data['phone_number']
            global_number = GlobalNumbers.objects.create(name=name, phone_number=phone_number, user=user)
            return Response({'message': 'Successfully SignedUp'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        name_or_phone = request.data.get('name_or_phone')
        password = request.data.get('password')

        if not name_or_phone or not password:
            return Response({'message': 'Both name and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if name_or_phone.isdigit():
                user = CustomUser.objects.get(phone_number=name_or_phone)
            else:
                user = CustomUser.objects.get(name=name_or_phone)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Invalid Login'}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            return Response({'message': 'Invalid Login'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'LogIn Successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)   
    

class MyConatactListAPIView(generics.ListCreateAPIView):
    serializer_class = GlobalNumbersSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the currently authenticated user
        user = self.request.user
        print('user',user)
        # Filter contacts that are not associated with the currently authenticated user
        queryset = GlobalNumbers.objects.filter(user=user)

        # Get search parameters from query parameters if provided
        name = self.request.query_params.get('name', None)
        phone_number = self.request.query_params.get('phone_number', None)

        # Apply search filter if search parameters are provided
        if name:
            queryset = queryset.filter(name__icontains=name)
        if phone_number:
            queryset = queryset.filter(phone_number__icontains=phone_number)

        return queryset
    


class ReportSpamAPIView(generics.CreateAPIView):
    serializer_class = GlobalNumbersSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a record with the provided phone number exists
        try:
            contact = GlobalNumbers.objects.get(phone_number=phone_number)
        except GlobalNumbers.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)

        # Mark the contact as spam
        contact.is_spam = True
        contact.save()

        return Response({'message': 'Phone number marked as spam successfully'}, status=status.HTTP_200_OK)


class GetAllSpamNumbersAPIView(generics.ListAPIView):
    queryset = GlobalNumbers.objects.filter(is_spam=True)
    serializer_class = GlobalNumbersSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]