from django.contrib import admin
from .models import Appointment, DoctorAvailability,Weekday

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'weekday','appointment_time','status']  # إظهار الطبيب، المريض، الموعد، والحالة في الـ Admin
    list_filter = ['doctor', 'status']  # يمكن تصفية المواعيد حسب الطبيب أو الحالة
    search_fields = ['doctor__username', 'patient__username']  # إضافة البحث حسب الطبيب أو المريض

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'available_from', 'available_to', 'get_days_of_week']

    def get_days_of_week(self, obj):
        return ", ".join([day.name for day in obj.days_of_week.all()])  # تحويل الأيام إلى نص مفصول بفواصل
    get_days_of_week.short_description = 'Days of Week'  # تغيير العنوان في الـ Admin

@admin.register(Weekday)
class WeekdayAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']