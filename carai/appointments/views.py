from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DoctorAvailability,CustomUser,Weekday
from .serializers import DoctorAvailabilitySerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta,date
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.db import transaction


class AvailableAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doctor_id, *args, **kwargs):
        doctor_availabilities = DoctorAvailability.objects.filter(doctor_id=doctor_id)

        if not doctor_availabilities:
            return Response({"message": "No available schedule found for this doctor."},
                            status=status.HTTP_404_NOT_FOUND)

        # تقسيم الساعات المتاحة للطبيب
        available_slots = []
        for availability in doctor_availabilities:
            for day in availability.days_of_week.all():
                start_time = availability.available_from
                end_time = availability.available_to

                # إضافة كل ساعة في اليوم كموعد
                while start_time < end_time:
                    available_slots.append({
                        "day": day.name,
                        "time": start_time.strftime("%H:%M"),
                        "is_booked": False  # هذا الحقل سنقوم بتحديثه لاحقًا بناءً على الحجز
                    })
                    start_time = (datetime.combine(date.today(), start_time) + timedelta(hours=1)).time()

        return Response({"available_slots": available_slots}, status=status.HTTP_200_OK)





class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ التأكد من أن المستخدم هو الطبيب """

        if self.request.user.role != 'doctor':
            return Response({"detail": "Only doctors can set availability."}, status=status.HTTP_403_FORBIDDEN)

        # تحديد الطبيب تلقائيًا بناءً على المستخدم المسجل
        serializer.save(doctor=self.request.user)

    def list(self, request, *args, **kwargs):
        """ إرجاع مواعيد الطبيب المسجل دخوله """
        if self.request.user.role != 'doctor':  # التحقق من أن المستخدم هو الطبيب فقط
            return Response({"detail": "Only doctors can view availability."}, status=status.HTTP_403_FORBIDDEN)

        # استخدام doctor_id من المستخدم الذي سجل الدخول (self.request.user)
        doctor_availabilities = DoctorAvailability.objects.filter(doctor=request.user)
        serializer = self.get_serializer(doctor_availabilities, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """ تعديل مواعيد التوافر للطبيب """
        availability = self.get_object()

        # التأكد من أن المستخدم هو الطبيب نفسه
        if availability.doctor != request.user:
            return Response({"detail": "You cannot modify another doctor's availability."},
                            status=status.HTTP_403_FORBIDDEN)


        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """ تعديل جزئي لمواعيد التوافر للطبيب """
        availability = self.get_object()

        # التأكد من أن المستخدم هو الطبيب نفسه
        if availability.doctor != request.user:
            return Response({"detail": "You cannot modify another doctor's availability."},
                            status=status.HTTP_403_FORBIDDEN)

        # إضافة منطق لتحديث التوافر فقط في حال عدم وجود تعارض مع مواعيد أخرى
        return super().partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ إرجاع توافر الطبيب بناءً على معرف الطبيب (ID) """
        # التحقق من أن المستخدم هو الطبيب فقط
        if request.user.role != 'doctor':
            return Response({"detail": "Only doctors can view their availability."}, status=status.HTTP_403_FORBIDDEN)

        availability = self.get_object()

        # التأكد من أن الطبيب يطلب التوافر الخاص به فقط
        if availability.doctor != request.user:
            return Response({"detail": "You cannot view availability for another doctor."}, status=status.HTTP_403_FORBIDDEN)

        return super().retrieve(request, *args, **kwargs)
    @action(detail=False, methods=['get'])
    def doctor_schedule(self, request):
        """ إرجاع جدول توافر الطبيب مع التحقق من المواعيد المحجوزة """
        # استخدام doctor_id من المستخدم الذي سجل الدخول (self.request.user)
        doctor = request.user

        if doctor.role != 'doctor':
            return Response({"error": "المستخدم ليس طبيبًا"}, status=400)

        # استرجاع توافر الطبيب من قاعدة البيانات
        doctor_availabilities = DoctorAvailability.objects.filter(doctor=doctor)
        schedule_data = []

        for availability in doctor_availabilities:
            available_times = []
            for day in availability.days_of_week.all():
                available_times.append({
                    "day": day.name,
                    "available_from": availability.available_from,
                    "available_to": availability.available_to,
                })
            schedule_data.append({"doctor": doctor.username, "schedule": available_times})

        return Response({"doctor_schedule": schedule_data})


# class AppointmentViewSet(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer
#
#     def perform_create(self, serializer):
#         # التأكد من أن المستخدم هو مريض (patient)
#         if self.request.user.role != 'patient':
#             return Response({"detail": "Only patients can book appointments."}, status=status.HTTP_403_FORBIDDEN)
#
#         # تحديد المريض تلقائيًا من المستخدم المسجل
#         patient = self.request.user  # المريض هو المستخدم الذي قام بتسجيل الدخول
#         doctor = serializer.validated_data['doctor']  # الطبيب الذي يود المريض حجز موعد معه
#         appointment_date = serializer.validated_data['appointment_date']  # الموعد الذي اختاره المريض
#
#         # التحقق من أن الموعد ضمن مواعيد الطبيب المتاحة
#         available_times = DoctorAvailability.objects.filter(doctor=doctor)
#         valid_appointment = False
#         for availability in available_times:
#             if availability.available_from <= appointment_date.time() <= availability.available_to:
#                 valid_appointment = True
#                 break
#
#         if not valid_appointment:
#             return Response({"detail": "The selected appointment time is not available."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         serializer.save(patient=patient, status='pending')


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'post'])
    def doctor_availability(self, request):
        """ إرجاع توافر الطبيب (الأيام المتاحة وساعات العمل) والتحقق من المواعيد المحجوزة """

        doctor_id = request.query_params.get('doctor_id')

        if not doctor_id:
            return Response({"error": "يجب إرسال doctor_id في URL"}, status=400)

        try:
            doctor = CustomUser.objects.get(id=doctor_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "الطبيب غير موجود"}, status=status.HTTP_404_NOT_FOUND)

        if doctor.role != 'doctor':
            return Response({"error": "المستخدم ليس طبيبًا"}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            # في حالة GET: عرض المواعيد المتاحة للطبيب
            doctor_availability = DoctorAvailability.objects.filter(doctor=doctor)

            if not doctor_availability:
                return Response({"error": "الطبيب ليس لديه مواعيد محددة"}, status=404)

            availability_data = []
            for availability in doctor_availability:
                for day in availability.days_of_week.all():
                    start_time = availability.available_from
                    end_time = availability.available_to
                    available_slots = []
                    booked_appointments = []

                    # تحويل start_time إلى datetime لتمكين التعديل عليه
                    current_time = datetime.combine(datetime.today(), start_time)

                    while current_time.time() < end_time:
                        available_slots.append(current_time.strftime("%H:%M:%S"))

                        # إضافة ساعة باستخدام timedelta
                        current_time += timedelta(hours=1)

                    # جلب المواعيد المحجوزة للطبيب في اليوم المحدد
                    appointments = Appointment.objects.filter(
                        doctor=doctor,
                        weekday=day,
                        status="completed"
                    )

                    booked_times = {appointment.appointment_time.strftime("%H:%M:%S") for appointment in appointments}
                    free_slots = [time for time in available_slots if time not in booked_times]
                    booked_appointments = [time for time in available_slots if time in booked_times]

                    availability_data.append({
                        "day": day.name,
                        "available_from": start_time.strftime("%H:%M:%S"),
                        "available_to": end_time.strftime("%H:%M:%S"),
                        "free_slots": free_slots,
                        "booked_slots": booked_appointments  # إضافة المواعيد المحجوزة
                    })

            return Response({"doctor_availability": availability_data})

        elif request.method == 'POST':
            day_name = request.data.get('day')
            time = request.data.get('time')
            patient = request.user

            if not day_name or not time:
                return Response({"error": "يجب إرسال اليوم و الموعد"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                day = Weekday.objects.get(name=day_name)
            except Weekday.DoesNotExist:
                return Response({"error": "اليوم غير موجود في جدول الأيام"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                appointment_time = datetime.strptime(time, "%H:%M:%S").time()
            except ValueError:
                return Response({"error": "الوقت المدخل غير صالح. يجب أن يكون بصيغة HH:MM:SS."},
                                status=status.HTTP_400_BAD_REQUEST)

            # استخدم معاملة لضمان الحجز بشكل صحيح
            with transaction.atomic():
                # التحقق إذا كان الموعد محجوزًا بالفعل للطبيب في نفس اليوم والوقت
                existing_appointments = Appointment.objects.filter(
                    doctor=doctor,
                    weekday=day,
                    appointment_time=appointment_time,
                    status="completed"
                )

                if existing_appointments.exists():
                    return Response({"error": "الموعد محجوز بالفعل للطبيب في هذا الوقت."},
                                    status=status.HTTP_400_BAD_REQUEST)

                # إذا كان الموعد متاحًا، نقوم بإنشاء الحجز
                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    weekday=day,
                    appointment_time=appointment_time,
                    status='completed'
                )

                # إعادة استرجاع المواعيد المحجوزة بعد الحجز مباشرة
                doctor_availability = DoctorAvailability.objects.filter(doctor=doctor)
                availability_data = []
                for availability in doctor_availability:
                    for day in availability.days_of_week.all():
                        start_time = availability.available_from
                        end_time = availability.available_to
                        available_slots = []
                        booked_appointments = []

                        current_time = datetime.combine(datetime.today(), start_time)

                        while current_time.time() < end_time:
                            available_slots.append(current_time.strftime("%H:%M:%S"))
                            current_time += timedelta(hours=1)

                        appointments = Appointment.objects.filter(
                            doctor=doctor,
                            weekday=day,
                            status="completed"
                        )

                        booked_times = {appointment.appointment_time.strftime("%H:%M:%S") for appointment in appointments}
                        free_slots = [time for time in available_slots if time not in booked_times]
                        booked_appointments = [time for time in available_slots if time in booked_times]

                        availability_data.append({
                            "day": day.name,
                            "available_from": start_time.strftime("%H:%M:%S"),
                            "available_to": end_time.strftime("%H:%M:%S"),
                            "free_slots": free_slots,
                            "booked_slots": booked_appointments
                        })

                # return Response({"doctor_availability": availability_data})
                return Response({
                    "message": "تم حجز المعاد بنجاح",
                    "doctor_availability": availability_data
                }, status=status.HTTP_201_CREATED)