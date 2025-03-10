from django.db import models
from register_user.models import CustomUser






class Weekday(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    # weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)  # إضافة هذا الحقل لربط اليوم
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE, null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    # appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Appointment of {self.patient.username} with {self.doctor.username} on {self.weekday}"


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="availability")
    available_from = models.TimeField()
    available_to = models.TimeField()
    days_of_week = models.ManyToManyField(Weekday, related_name="available_doctors")

    def __str__(self):
        return f"{self.doctor.username} Availability from {self.available_from} to {self.available_to} on {', '.join([day.name for day in self.days_of_week.all()])}"

