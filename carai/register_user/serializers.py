from rest_framework_simplejwt.tokens import RefreshToken
from rest_registration.api.serializers import DefaultRegisterUserSerializer,DefaultLoginSerializer
from .models import CustomUser, Specialization
from rest_framework import serializers
from rating.models import DoctorReview
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


#Karim
# send email and notification after change password
import jwt  # تأكد من استيراد jwt
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import BlacklistedAccessToken ,BlacklistedRefreshToken   # أضف هذا السطر
# from rest_registration.verification_notifications import send_register_email_verification_email_notification
from rest_registration.signers.register import RegisterSigner
from register_user.models import CustomUser  # تأكد من استيراد الموديل الخاص بالمستخدمين

# Karim

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # ✅ استرجاع بيانات تسجيل الدخول
        login_field = attrs.get("username") or attrs.get("email")  # دعم email أو username
        password = attrs.get("password")

        if not login_field or not password:
            raise AuthenticationFailed("يجب إدخال البريد الإلكتروني أو اسم المستخدم وكلمة المرور.", code='authorization')

        # ✅ البحث عن المستخدم باستخدام email أو username
        user = CustomUser.objects.filter(email=login_field).first() or \
               CustomUser.objects.filter(username=login_field).first()

        # ✅ التحقق من صحة البيانات وكلمة المرور
        if not user or not user.check_password(password):
            raise AuthenticationFailed("الحساب غير موجود أو البيانات غير صحيحة.", code='authorization')

        # ✅ منع تسجيل الدخول إذا لم يتم تفعيل الحساب
        if not user.is_active:
            raise AuthenticationFailed("يجب عليك تفعيل حسابك عبر البريد الإلكتروني قبل تسجيل الدخول.", code='authorization')

        # ✅ منع الأطباء من تسجيل الدخول قبل موافقة الأدمن
        if user.role == 'doctor' and not user.is_approved:
            raise AuthenticationFailed("حسابك قيد المراجعة من قبل الإدارة.", code='authorization')

        # ✅ تسجيل دخول المستخدم باستخدام authenticate()
        authenticated_user = authenticate(email=user.email, password=password)

        if authenticated_user is None:
            raise AuthenticationFailed("No active account found with the given credentials")

        # ✅ إنشاء التوكنز
        refresh = self.get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        }

        return data


# Karim

# ✅ تسجيل المستخدمين الجدد
class CustomRegisterUserSerializer(serializers.ModelSerializer):
    specialization = serializers.PrimaryKeyRelatedField(
        queryset=Specialization.objects.all(),
        required=False,
        allow_null=True
    )
    consultation_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True
    )
    location = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone_number', 'password',
            'gender', 'age', 'role', 'specialization', 'consultation_price', 'location'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("البريد الإلكتروني مسجل مسبقًا.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data['is_active'] = False  

        specialization = validated_data.pop('specialization', None)
        user = CustomUser.objects.create(**validated_data)

        if user.role == 'doctor':
            user.is_approved = False
            user.specialization = specialization

        # ✅ إرسال إيميل التحقق
        signer = RegisterSigner({'user_id': user.id})
        # send_register_email_verification_email_notification(
        #     self.context["request"],
        #     user,
        #     user.email
        # )

        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        return {
            "message": f"Welcome, {instance.username}. Please check your email to verify your account."
        }



# change password >>> send notification and email after change password >>> Cutomized

class CustomChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "New passwords do not match."})
        try:
            validate_password(data['new_password'], self.context['request'].user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        
        return data
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

        # إضافة الـ access_token إلى القائمة السوداء
        auth_header = self.context['request'].headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            access_token = auth_header.split(" ")[1]
            try:
                decoded_token = jwt.decode(access_token, options={"verify_signature": False})
                jti = decoded_token.get("jti")
                if not BlacklistedAccessToken.objects.filter(jti=jti).exists():
                    BlacklistedAccessToken.objects.create(jti=jti)  # استخدام jti فقط
            except jwt.ExpiredSignatureError:
                raise serializers.ValidationError({"error": "Token has expired"})
            except jwt.InvalidTokenError:
                raise serializers.ValidationError({"error": "Invalid token"})

        # إضافة الـ refresh_token إلى القائمة السوداء
        refresh_token = self.context['request'].data.get('refresh')
        if refresh_token:
            try:
                decoded_refresh_token = jwt.decode(refresh_token, options={"verify_signature": False})
                refresh_jti = decoded_refresh_token.get("jti")
                if not BlacklistedRefreshToken.objects.filter(jti=refresh_jti).exists():
                    BlacklistedRefreshToken.objects.create(jti=refresh_jti)  # استخدام jti فقط
            except jwt.ExpiredSignatureError:
                raise serializers.ValidationError({"error": "Refresh token has expired"})
            except jwt.InvalidTokenError:
                raise serializers.ValidationError({"error": "Invalid refresh token"})


                

        # إرسال إيميل بعد تغيير كلمة المرور
        context = {'user': user}
        subject = render_to_string('rest_registration/password_changed/subject.txt', context).strip()
        message = render_to_string('rest_registration/password_changed/body.txt', context)

        send_mail(
            subject=subject,
            message=message,
            from_email=None,  # سيتم استخدام DEFAULT_FROM_EMAIL في settings
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({"detail": "Password changed successfully. Please log in again."}, status=status.HTTP_200_OK)

    # def save(self, **kwargs):
    #     user = self.context['request'].user
    #     user.set_password(self.validated_data['new_password'])
    #     user.save()

    #     # ✅ إرسال إيميل بعد تغيير كلمة المرور
    #     context = {'user': user}
    #     subject = render_to_string('rest_registration/password_changed/subject.txt', context).strip()
    #     message = render_to_string('rest_registration/password_changed/body.txt', context)

    #     send_mail(
    #         subject=subject,
    #         message=message,
    #         from_email=None,  # سيتم استخدام DEFAULT_FROM_EMAIL في settings
    #         recipient_list=[user.email],
    #         fail_silently=False,
    #     )

    #     return user

#rate serializers
class DoctorReviewSerializer(serializers.ModelSerializer):
    patient_username = serializers.CharField(source='patient.username', read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = DoctorReview
        fields = ['patient_username', 'rating', 'comment', 'created_at']
        ref_name = 'RegisterUserDoctorReviewSerializer'  # تحديد ref_name بشكل صريح

# show Specialization with doctor is_approved
class DoctorSerializer(serializers.ModelSerializer):
    reviews = DoctorReviewSerializer(source='doctor_reviews', many=True, read_only=True)  # إضافة التقييمات للطبيب
    specialization = serializers.CharField(source='specialization.name', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'specialization', 'consultation_price', 'location', 'reviews']


# 'http://127.0.0.1:8000/specializations/ >>> اسم التخصص 
class SpecializationListSerializer(serializers.ModelSerializer):
    doctor_count = serializers.SerializerMethodField()

    class Meta:
        model = Specialization
        fields = ['id', 'name', 'doctor_count']

    def get_doctor_count(self, obj):
        """إرجاع عدد الأطباء الموافق عليهم في هذا التخصص"""
        return CustomUser.objects.filter(specialization=obj, role='doctor', is_approved=True).count()

class SpecializationDetailSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer(source='customuser_set', many=True, read_only=True)

    class Meta:
        model = Specialization
        fields = ['id', 'name', 'doctors']
    def get_doctors(self, obj):
        """إرجاع قائمة الأطباء الموافق عليهم فقط داخل هذا التخصص"""
        approved_doctors = CustomUser.objects.filter(specialization=obj, role='doctor', is_approved=True)
        return DoctorSerializer(approved_doctors, many=True).data
