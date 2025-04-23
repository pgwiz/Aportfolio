# authentication/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import PortfolioUser
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer
)

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create user with hashed password
        user = PortfolioUser.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=serializer.validated_data['password']
        )
        
        # Generate tokens for immediate login
        token_serializer = CustomTokenObtainPairSerializer(data={
            'username': user.username,
            'password': serializer.validated_data['password']
        })
        token_serializer.is_valid(raise_exception=True)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': token_serializer.validated_data
        }, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        
        # Handle password change separately
        if 'password' in request.data:
            instance.set_password(request.data['password'])
            instance.save()
        
        self.perform_update(serializer)
        return Response(serializer.data)
        
        
from rest_framework.views import APIView  # Add this import
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PortfolioUser, UserPreference

class ThemePreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pref = request.user.userpreference  # Make sure the related_name matches
        return Response({'dark_mode': pref.dark_mode})

    def post(self, request):
        pref = request.user.userpreference
        pref.dark_mode = not pref.dark_mode
        pref.save()
        return Response({'dark_mode': pref.dark_mode})
            
            
from rest_framework import viewsets
from .models import PortfolioUser
from .serializers import UserSerializer

class PortfolioUserViewSet(viewsets.ModelViewSet):
    queryset = PortfolioUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only allow admins to modify users

    def get_queryset(self):
        # Only show current user unless admin
        if self.request.user.is_staff:
            return PortfolioUser.objects.all()
        return PortfolioUser.objects.filter(id=self.request.user.id)          