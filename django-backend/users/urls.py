from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, UserProfileView, 
    MedicalProfileView, CreateMedicalProfileView, 
    UpdateMedicalProfileView, 
    DiaryListView, GoalListView, NotificationListView, 
    CreateDiaryView, CreateGoalView , UpdateUserProfileView, CreateUserProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/get/', UserProfileView.as_view(), name='user-profile'), # get user profile
    path('profile/create', CreateUserProfileView.as_view(), name='user-create'), # create user profile
    path('profile/update', UpdateUserProfileView.as_view(), name='user-update'), # update user profile
    
    path('medical-info/', MedicalProfileView.as_view(), name='medical-info'), # get medical info
    path('medical-profile/create/', CreateMedicalProfileView.as_view(), name='create-medical-profile'), # create medical profile
    path('medical-profile/update/', UpdateMedicalProfileView.as_view(), name='update-medical-profile'),  # update medical profile
    
    path('diary/', DiaryListView.as_view(), name='diary-list'), # get diary list
    path('diary/create', CreateDiaryView.as_view(), name='create-diary'), # create diary

    path('goal/', GoalListView.as_view(), name='goal-list'), # get goal list
    path('add-goal', CreateGoalView.as_view(), name='goal-add'), # add goal

    path('notifications/', NotificationListView.as_view(), name='notification-list'),
]