from rest_framework import status,viewsets, permissions, generics,filters
from rest_framework.response import Response
from rest_framework.decorators import action,permission_classes,api_view
from django.shortcuts import get_object_or_404
from .models import Specialization, CustomUser,BlacklistedAccessToken ,BlacklistedRefreshToken
from .serializers import SpecializationListSerializer, SpecializationDetailSerializer, DoctorSerializer , CustomChangePasswordSerializer
from .filters import SpecializationFilter, DoctorFilter
from django_filters.rest_framework import DjangoFilterBackend
from .Pagination import DoctorPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
import jwt
# Cahcing
# from .tasks import send_password_change_email
# from django.core.cache import cache
#Karim
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken



class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# class LogoutView(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data.get('refresh')
#             if not refresh_token:
#                 return Response({'error':'refresh is required'}, status=status.HTTP_400_BAD_REQUEST)

#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

            # إضافة الـ refresh_token إلى القائمة السوداء
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # إضافة الـ refresh_token إلى القائمة السوداء
            except Exception as e:
                return Response({"error": f"Invalid refresh token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            # إضافة الـ access_token إلى القائمة السوداء
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                access_token = auth_header.split(" ")[1]
                try:
                    decoded_token = jwt.decode(access_token, options={"verify_signature": False})
                    jti = decoded_token.get("jti")
                    if not BlacklistedAccessToken.objects.filter(jti=jti).exists():
                        BlacklistedAccessToken.objects.create(jti=jti)
                except jwt.ExpiredSignatureError:
                    return Response({"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)
                except jwt.InvalidTokenError:
                    return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

  
# دا التعديل بتاع تغير الباسورد وكدا بعد معملنا وكدا DEAFULT CHANGE PASSWORD مخصص لينا احنا بدل المكتبه الاساسيه الللي بنسدخمها وكدا
# class ChangePasswordView(generics.UpdateAPIView):
#     serializer_class = CustomChangePasswordSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def update(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         # ✅ استخراج `Access Token` من الهيدر
#         auth_header = request.headers.get("Authorization", "")
#         if auth_header.startswith("Bearer "):
#             access_token = auth_header.split(" ")[1]
#             decoded_token = AccessToken(access_token)
#             jti = decoded_token["jti"]

#             # ✅ إضافة التوكن إلى القائمة السوداء
#             BlacklistedAccessToken.objects.create(jti=jti)

#         return Response({"detail": "Password changed successfully. Please log in again."}, status=status.HTTP_200_OK)   

# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# def change_password(request):
#     # الحصول على المستخدم الحالي من الطلب
#     user = request.user
#     serializer = CustomChangePasswordSerializer(data=request.data, context={"request": request})

#     if serializer.is_valid(raise_exception=True):
#         # حفظ كلمة المرور الجديدة
#         serializer.save()

#         # إضافة الـ access_token إلى القائمة السوداء
#         auth_header = request.headers.get("Authorization", "")
#         if auth_header.startswith("Bearer "):
#             access_token = auth_header.split(" ")[1]
#             try:
#                 decoded_token = jwt.decode(access_token, options={"verify_signature": False})
#                 jti = decoded_token.get("jti")
#                 if not BlacklistedAccessToken.objects.filter(jti=jti).exists():
#                     BlacklistedAccessToken.objects.create(jti=jti)
#             except jwt.ExpiredSignatureError:
#                 return Response({"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)
#             except jwt.InvalidTokenError:
#                 return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

#         # إضافة الـ refresh_token إلى القائمة السوداء
#         refresh_token = request.data.get('refresh')
#         if refresh_token:
#             try:
#                 decoded_refresh_token = jwt.decode(refresh_token, options={"verify_signature": False})
#                 refresh_jti = decoded_refresh_token.get("jti")
#                 if not BlacklistedRefreshToken.objects.filter(jti=refresh_jti).exists():
#                     BlacklistedRefreshToken.objects.create(jti=refresh_jti)
#             except jwt.ExpiredSignatureError:
#                 return Response({"error": "Refresh token has expired"}, status=status.HTTP_400_BAD_REQUEST)
#             except jwt.InvalidTokenError:
#                 return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

#         # إرسال إيميل بعد تغيير كلمة المرور
#         context = {'user': user}
#         subject = render_to_string('rest_registration/password_changed/subject.txt', context).strip()
#         message = render_to_string('rest_registration/password_changed/body.txt', context)

#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=None,  # سيتم استخدام DEFAULT_FROM_EMAIL في settings
#             recipient_list=[user.email],
#             fail_silently=False,
#         )

#         return Response({"detail": "Password changed successfully. Please log in again."}, status=status.HTTP_200_OK)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = CustomChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # منع استخدام PUT
        return Response(
            {"detail": "Method PUT not allowed. Use PATCH instead."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def patch(self, request, *args, **kwargs):
        # السماح فقط بـ PATCH
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # إضافة الـ access_token إلى القائمة السوداء
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            access_token = auth_header.split(" ")[1]
            try:
                decoded_token = jwt.decode(access_token, options={"verify_signature": False})
                jti = decoded_token.get("jti")
                if not BlacklistedAccessToken.objects.filter(jti=jti).exists():
                    BlacklistedAccessToken.objects.create(jti=jti)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        # إضافة الـ refresh_token إلى القائمة السوداء
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                decoded_refresh_token = jwt.decode(refresh_token, options={"verify_signature": False})
                refresh_jti = decoded_refresh_token.get("jti")
                if not BlacklistedRefreshToken.objects.filter(jti=refresh_jti).exists():
                    BlacklistedRefreshToken.objects.create(jti=refresh_jti)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Refresh token has expired"}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Password changed successfully. Please log in again."}, status=status.HTTP_200_OK)

class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialization.objects.all().order_by('name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SpecializationFilter
    search_fields = ['name']
    permission_classes = [AllowAny]
    pagination_class = None

    def get_serializer_class(self):
        """استخدام `SpecializationListSerializer` للقائمة و `SpecializationDetailSerializer` عند تحديد تخصص"""
        if self.action == 'list':
            return SpecializationListSerializer
        return SpecializationDetailSerializer

    @action(detail=True, methods=['get'])
    def doctors(self, request, pk=None):
        """إرجاع جميع الأطباء المرتبطين بتخصص معين"""
        specialization = self.get_object()
        doctors = CustomUser.objects.filter(specialization=specialization, role='doctor', is_approved=True)

        filtered_doctors = DoctorFilter(request.GET, queryset=doctors).qs  # تطبيق الفلاتر هنا

        if not filtered_doctors.exists():
            return Response({"message": "No approved doctors found for this specialization."}, status=200)

        serializer = DoctorSerializer(filtered_doctors, many=True)  # استخدام الأطباء بعد الفلترة
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='doctors/(?P<doctor_id>[^/.]+)')
    def doctor_detail(self, request, pk=None, doctor_id=None):
        """إرجاع بيانات طبيب معين داخل تخصص معين"""
        specialization = self.get_object()
        doctor = get_object_or_404(CustomUser, id=doctor_id, specialization=specialization, role='doctor', is_approved=True)

        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)



class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(role='doctor', is_approved=True)
    serializer_class = DoctorSerializer
    pagination_class = DoctorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DoctorFilter
    search_fields = ['username', 'location', 'specialization__name']

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    




# Caching For serializers

# class CachedSpecializationView(APIView):
#     def get(self, request):
#         cache_key = "specializations_list"
#         cached_data = cache.get(cache_key)

#         if cached_data is not None:
#             return Response(cached_data)  # رجّع البيانات من الكاش مباشرةً

#         specializations = Specialization.objects.all()
#         serializer = SpecializationListSerializer(specializations, many=True)

#         cache.set(cache_key, serializer.data, timeout=60 * 200)  # تخزين البيانات في الكاش لمدة 200 دقيقة
#         return Response(serializer.data)
# class CachedSpecializationDetailView(APIView):
#     def get(self, request, specialization_id):
#         cache_key = f"specialization_detail_{specialization_id}"
#         cached_data = cache.get(cache_key)

#         if cached_data is not None:
#             return Response(cached_data)  # رجّع البيانات من الكاش مباشرةً

#         specialization = Specialization.objects.get(id=specialization_id)
#         serializer = SpecializationDetailSerializer(specialization)

#         cache.set(cache_key, serializer.data, timeout=60 * 200)  # تخزين البيانات في الكاش لمدة 200 دقيقة
#         return Response(serializer.data)


# class CachedDoctorView(APIView):
#     def get(self, request):
#         cache_key = f"doctors_list_{request.GET.urlencode()}"  # مفتاح ديناميكي حسب الفلاتر
#         cached_data = cache.get(cache_key)

#         if cached_data is not None:
#             return Response(cached_data)  # رجّع البيانات من الكاش مباشرةً

#         doctors = CustomUser.objects.filter(role="doctor", is_approved=True)

#         # تطبيق الفلاتر
#         filtered_doctors = DoctorFilter(request.GET, queryset=doctors).qs

#         serializer = DoctorSerializer(filtered_doctors, many=True)
#         cache.set(cache_key, serializer.data, timeout=60 * 200)  # تخزين البيانات في الكاش لمدة 200 دقيقة
#         return Response(serializer.data)

# class CachedSpecializationDetailView(APIView):
#     def get(self, request, specialization_id):
#         cache_key = f"specialization_detail_{specialization_id}"
#         cached_data = cache.get(cache_key)

#         if cached_data is not None:
#             return Response(cached_data)  # رجّع البيانات من الكاش مباشرةً

#         # استخدام get_object_or_404 بدلاً من get لتجنب الأخطاء
#         specialization = get_object_or_404(Specialization, id=specialization_id)
#         serializer = SpecializationDetailSerializer(specialization)

#         cache.set(cache_key, serializer.data, timeout=60 * 200)  # تخزين البيانات في الكاش لمدة 200 دقيقة
#         return Response(serializer.data)


# class CachedDoctorViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.filter(role="doctor", is_approved=True)
#     serializer_class = DoctorSerializer

#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         cache.delete("doctors_list")  # حذف الكاش بعد الإضافة
#         return response
