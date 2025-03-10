# from celery import shared_task
# from django.core.mail import send_mail
# from django.template.loader import render_to_string

# @shared_task
# def send_email_verification(user_email, username):
#     """إرسال إيميل تفعيل الحساب"""
#     context = {'username': username}
#     subject = render_to_string('rest_registration/register/subject.txt', context).strip()
#     message = render_to_string('rest_registration/register/body.txt', context)

#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=None,  # سيستخدم DEFAULT_FROM_EMAIL من الإعدادات
#         recipient_list=[user_email],
#         fail_silently=False,
#     )

# @shared_task
# def send_password_change_email(user_email, username):
#     """إرسال إيميل تأكيد تغيير الباسورد"""
#     context = {'username': username}
#     subject = render_to_string('rest_registration/password_changed/subject.txt', context).strip()
#     message = render_to_string('rest_registration/password_changed/body.txt', context)

#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=None,
#         recipient_list=[user_email],
#         fail_silently=False,
#     )

# @shared_task
# def send_reset_password_email(user_email, reset_link):
#     """إرسال إيميل إعادة تعيين الباسورد"""
#     context = {'reset_link': reset_link}
#     subject = render_to_string('rest_registration/reset_password/subject.txt', context).strip()
#     message = render_to_string('rest_registration/reset_password/body.txt', context)

#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=None,
#         recipient_list=[user_email],
#         fail_silently=False,
#     )

# @shared_task
# def send_email_change_verification(user_email, username):
#     """إرسال إيميل تأكيد تغيير الإيميل"""
#     context = {'username': username}
#     subject = render_to_string('rest_registration/register_email/subject.txt', context).strip()
#     message = render_to_string('rest_registration/register_email/body.txt', context)

#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=None,
#         recipient_list=[user_email],
#         fail_silently=False,
#     )
