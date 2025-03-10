from django.contrib import admin
from django.apps import apps
from .models import CustomUser,Specialization


class IsApprovedFilter(admin.SimpleListFilter):
    """فلتر مخصص لعرض المستخدمين غير الموافق عليهم"""
    title = 'Approval Status'  # عنوان الفلتر في Django Admin
    parameter_name = 'is_approved'

    def lookups(self, request, model_admin):
        """تحديد الخيارات داخل الفلتر"""
        return [
            ('approved', 'Approved'),
            ('not_approved', 'Not Approved'),
        ]

    def queryset(self, request, queryset):
        """تحديد الفلترة بناءً على الخيار المختار"""
        if self.value() == 'approved':
            return queryset.filter(is_approved=True)
        elif self.value() == 'not_approved':
            return queryset.filter(is_approved=False)
        return queryset

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'age', 'gender','role','specialization','is_approved','is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'gender', 'role', 'specialization', IsApprovedFilter)  # إضافة الفلتر الجديد
    ordering = ('-date_joined',)
    actions = ['approve_doctors']


    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'age', 'gender')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_approved')
        }),
    )

    def approve_doctors(self, request, queryset):
        doctors = queryset.filter(role='doctor', is_approved=False)
        if doctors.exists():
            count = doctors.count()
            doctors.update(is_approved=True, is_active=True)
            self.message_user(request, f"Successfully approved {count} doctor(s)!")
        else:
            self.message_user(request, "No doctors found that require approval.", level='info')

    approve_doctors.short_description = "Approve selected doctors"


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')