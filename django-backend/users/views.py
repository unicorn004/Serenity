from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, MedicalProfile, Diary, Goal, Notification
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.utils.dateparse import parse_datetime
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, 
    UserProfileSerializer, MedicalProfileSerializer, 
    DiarySerializer, GoalSerializer, NotificationSerializer
)
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            # Try to get the user's profile
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            # If the profile does not exist, raise a 404 error
            raise NotFound("UserProfile not found.")
        
        return profile
class CreateUserProfileView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        # Associate the UserProfile with the currently authenticated user
        serializer.save(user=self.request.user)
        
# class UpdateUserProfileView(generics.UpdateAPIView):
#     serializer_class = UserProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         try:
#             user_profile = UserProfile.objects.get(user=self.request.user)
#         except UserProfile.DoesNotExist:
#             user_profile = UserProfile.objects.create(user=self.request.user)
        
#         return user_profile

class MedicalProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MedicalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        medical_profile = MedicalProfile.objects.get(user=user_profile)
        return medical_profile

class CreateMedicalProfileView(generics.CreateAPIView):
    serializer_class = MedicalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        medical_profile, created = MedicalProfile.objects.get_or_create(user=user_profile)
        if created:
            serializer.save(user=user_profile)
        else:
            return Response({"detail": "Medical Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateMedicalProfileView(generics.UpdateAPIView):
    serializer_class = MedicalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return user_profile.medical_profile


class DiaryListView(generics.ListCreateAPIView):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = UserProfile.objects.get(user=self.request.user)
        return Diary.objects.filter(user=profile)

class GoalListView(generics.ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = UserProfile.objects.get(user=self.request.user)
        return Goal.objects.filter(user=profile)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
class CreateDiaryView(generics.CreateAPIView):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(user=profile)

class CreateGoalView(generics.CreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(user=profile)


class UpdateUserProfileView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve the authenticated user's profile."""
        return get_object_or_404(UserProfile, user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Handle updates for various user profile attributes."""
        user_profile = self.get_object()
        data = request.data  # Data sent from frontend

        try:
            if "daily_mood" in data:
                user_profile.update_daily_mood(data["daily_mood"])

            if "wellness_score" in data:
                user_profile.update_wellness_score(data["wellness_score"])

            if "badge" in data:
                user_profile.add_badge(data["badge"])

            if "habit" in data and "performed_date" in data:
                performed_date = datetime.strptime(data["performed_date"], "%Y-%m-%d").date()
                user_profile.update_habit_streak(data["habit"], performed_date)

            if "sleep_quality" in data:
                user_profile.update_sleep_quality(data["sleep_quality"])

            if "activity_level" in data:
                user_profile.update_activity_level(data["activity_level"])

            if "mindfulness_level" in data:
                user_profile.update_mindfulness_level(data["mindfulness_level"])

            if "streak" in data:
                user_profile.update_streak(data["streak"])

            if "last_login" in data:
                new_last_login = parse_datetime(data["last_login"])
                if new_last_login:
                    user_profile.update_last_login(new_last_login)

            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)