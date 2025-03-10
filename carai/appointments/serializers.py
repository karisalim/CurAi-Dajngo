from rest_framework import serializers
from .models import Appointment,DoctorAvailability,Weekday
from datetime import datetime

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source='patient.username', read_only=True)
    doctor = serializers.CharField(source='doctor.username', read_only=True)  # عرض اسم الطبيب
    status = serializers.CharField(read_only=True)
    day = serializers.CharField(write_only=True)  # اليوم مثل Sunday
    time = serializers.CharField(write_only=True)  # الموعد مثل 06:00:00

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'day', 'time']

    def create(self, validated_data):
        """
        Override the create method to handle the conversion of `day` and `time`
        to `appointment_date`.
        """
        # الحصول على اليوم و الوقت من validated_data
        day = validated_data.pop('day')
        time = validated_data.pop('time')

        # تحويل اليوم و الوقت إلى تاريخ كامل
        appointment_date_str = f"{day} {time}"
        appointment_date = datetime.strptime(appointment_date_str, "%A %H:%M:%S")

        # إضافة `appointment_date` إلى validated_data
        validated_data['appointment_date'] = appointment_date

        # إنشاء الموعد باستخدام `appointment_date` و البيانات الأخرى
        appointment = super().create(validated_data)
        return appointment

class WeekdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekday
        fields = ['name']


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.username', read_only=True)
    days_of_week = serializers.ListField(
        child=serializers.CharField(max_length=20),
        write_only=True
    )

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'available_from', 'available_to', 'days_of_week']

    def create(self, validated_data):
        days_of_week = validated_data.pop('days_of_week', [])
        instance = super().create(validated_data)

        # إضافة الأيام المتاحة للمواعيد
        instance.days_of_week.set(
            Weekday.objects.filter(name__in=days_of_week)
        )

        return instance

    def to_representation(self, instance):
        """عرض أسماء الأيام في استجابة الـ API"""
        representation = super().to_representation(instance)
        # تحويل الـ ManyToManyField إلى أسماء الأيام مباشرة
        representation['days_of_week'] = [day.name for day in instance.days_of_week.all()]
        return representation