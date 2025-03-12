from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecializationViewSet,DoctorViewSet,LogoutView,LoginView ,ChangePasswordView  
from rest_registration.api.views import(
    login,
    register,
    profile,
    reset_password,
    send_reset_password_link,
    register_email,
    verify_email,
    verify_registration,    
    ) 

app_name = "register_user"
router = DefaultRouter()
router.register(r'specializations', SpecializationViewSet, basename='specialization')
router.register(r'All_doctors', DoctorViewSet, basename='doctor')



urlpatterns = [
    # path("api/auth/", include("rest_registration.api.urls")),
    # path("api/login/", login, name="login"),
    path("api/login/", LoginView.as_view(), name="login"),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/register/', register, name='register'),
    path('api/profile/', profile, name='profile'),

    path('', include(router.urls)),
    
    
    
    # ✅ **إضافة مسارات إعادة تعيين كلمة المرور وتغييرها**
    path("api/reset-password/", reset_password, name="reset-password"),
    path("api/send-reset-password-link/", send_reset_password_link, name="send-reset-password-link"),
    # path('api/change-password/', change_password, name='change-password'),
    
    # Custimze for change password
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),



    # ✅ **إضافة مسارات تسجيل البريد الإلكتروني والتحقق منه**
    path("api/verify-registration/", verify_registration, name="verify-registration"),
    path("api/register-email/", register_email, name="register-email"),
    path("api/verify-email/", verify_email, name="verify-email"),
    
    
        # ✅ كاشنج الـ Specializations
    # path("api/cached-specializations/", CachedSpecializationView.as_view(), name="cached-specializations"),
    # path("api/cached-specializations/<int:specialization_id>/", CachedSpecializationDetailView.as_view(), name="cached-specialization-detail"),

    # Cahcing Karim
    # path("api/cached-doctors/", CachedDoctorView.as_view(), name="cached-doctors"),
    
    

    
]


