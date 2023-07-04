from django.urls import path
from stportal import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView


urlpatterns = [

    path('',views.api_root,name='index'),
    path('reg/',views.RegistrationView.as_view(),name='reg'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('refreshtoken/',TokenRefreshView.as_view(),name='token_refresh'),
    path('logout/',views.LogoutView.as_view()),
    path('dashboard/<int:id>/',views.DashboardView.as_view(),name='dashboard'),

]
