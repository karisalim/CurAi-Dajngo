from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, AvailableAppointmentsView,DoctorAvailabilityViewSet

app_name = "appointments"

router = DefaultRouter()
router.register(r'patient_panal_appointments', AppointmentViewSet)
router.register(r'doctor_panal_availabilities', DoctorAvailabilityViewSet, basename='doctor-availability')

urlpatterns = [
    path('available_appointments/<int:doctor_id>/', AvailableAppointmentsView.as_view(), name='available_appointments'),
    path('', include(router.urls)),
]