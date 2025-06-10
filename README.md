# 🏥 Medical Appointment System

A comprehensive web-based medical appointment system built with Django that connects patients with doctors, enabling easy appointment scheduling, patient history tracking, and doctor reviews.

## ✨ Features

### 👥 User Management
- **🔐 Role-based Authentication**
  - Doctor registration and verification
  - Patient registration
  - Admin dashboard
  - Secure JWT authentication
  - Password reset functionality

- **👤 Profile Management**
  - Personal information management
  - Profile picture upload
  - Contact information
  - Location settings
  - Specialization details (for doctors)

### 👨‍⚕️ Doctor Features
- **📋 Profile Management**
  - Specialization selection
  - Consultation price setting
  - Professional certificate upload
  - Location management with GPS coordinates
  - Professional bio
  - Consultation hours

- **📅 Appointment Management**
  - Availability calendar
  - Appointment scheduling
  - Patient history tracking
  - Consultation notes
  - Payment tracking

### 👨‍💼 Patient Features
- **🔍 Search and Discovery**
  - Doctor search by specialization
  - Location-based search
  - Price filtering
  - Rating-based sorting
  - Availability checking

- **📱 Appointment Management**
  - Online booking
  - Appointment history
  - Medical records
  - Payment processing
  - Appointment reminders

- **⭐ Review System**
  - Doctor rating
  - Written reviews
  - Rating history
  - Review management

### 👨‍💻 Admin Features
- **👥 User Management**
  - User verification
  - Account management
  - Role assignment
  - Content moderation

- **⚙️ System Management**
  - Specialization management
  - System configuration
  - Analytics dashboard
  - Report generation

## 🛠️ Technical Stack

### 🔧 Backend
- **Framework**: Django 5.1.6
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Task Queue**: Celery (for background tasks)

### 🎨 Frontend
- **Admin Interface**: Django Material Admin
- **API Documentation**: Swagger/ReDoc
- **File Storage**: Local storage (Development) / Cloud storage (Production)

### 🔌 Additional Features
- CORS support for cross-origin requests
- API documentation with drf-yasg
- Material Design admin interface
- File upload handling
- Email notifications
- SMS notifications (optional)
- Payment gateway integration

## 🔐 Security Configuration (Production)

### ⚠️ Critical Security Settings
```python
# Never expose SECRET_KEY or use DEBUG=True in production!
DEBUG = False
SECRET_KEY = 'your-secure-secret-key'  # Store in environment variables

# SSL/HTTPS Configuration
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
REFERRER_POLICY = 'same-origin'

# Optional: Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_SCRIPT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:", "https:")
```

### 🔒 Comprehensive Security Settings

#### 1. Basic Security Settings
```python
# Debug and Secret Key
DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Allowed Hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database Security
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}
```

#### 2. Session Security
```python
# Session Configuration
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# CSRF Protection
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
CSRF_USE_SESSIONS = True
```

#### 3. Password Security
```python
# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Password Hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

#### 4. File Upload Security
```python
# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

#### 5. Email Security
```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

#### 6. Advanced Security Headers
```python
# Security Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'", "data:", "https:", "blob:")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_CONNECT_SRC = ("'self'", "https://api.yourdomain.com")
CSP_MEDIA_SRC = ("'self'", "https://media.yourdomain.com")
CSP_OBJECT_SRC = ("'none'",)
CSP_FRAME_SRC = ("'self'", "https://trusted-frame.com")
CSP_REPORT_URI = '/csp-report/'
```

#### 7. CORS and API Security
```python
# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://api.yourdomain.com",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# REST Framework Security
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

#### 8. Logging and Monitoring
```python
# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/security.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

### 📝 Security Best Practices

1. **Environment Variables**
   - Store all sensitive data in environment variables
   - Never commit `.env` files to version control
   - Use different environment variables for development and production

2. **Regular Updates**
   - Keep Django and all dependencies updated
   - Regularly check for security vulnerabilities
   - Subscribe to Django security mailing list

3. **Backup Strategy**
   - Implement regular database backups
   - Store backups in secure, encrypted locations
   - Test backup restoration regularly

4. **Monitoring**
   - Set up error monitoring (e.g., Sentry)
   - Monitor failed login attempts
   - Track suspicious activities
   - Set up alerts for security events

5. **Server Security**
   - Use a reverse proxy (e.g., Nginx)
   - Configure firewall rules
   - Enable SSL/TLS
   - Regular security audits

6. **Application Security**
   - Implement rate limiting
   - Use secure password hashing
   - Enable two-factor authentication
   - Regular security testing

7. **Data Protection**
   - Encrypt sensitive data
   - Implement data retention policies
   - Regular data cleanup
   - GDPR compliance measures

## 🛡️ Permissions

### 🔒 Default Permission Classes
The system uses Django REST Framework's permission classes for access control:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

### 👥 Built-in Permission Classes
- `AllowAny`: Allows unrestricted access
- `IsAuthenticated`: Requires user authentication
- `IsAdminUser`: Restricts access to admin users only
- `IsAuthenticatedOrReadOnly`: Allows read access to unauthenticated users
- `DjangoModelPermissions`: Ties into Django's standard `django.contrib.auth` model permissions
- `DjangoModelPermissionsOrAnonReadOnly`: Similar to above but allows anonymous read access
- `DjangoObjectPermissions`: Ties into Django's standard object-level permissions

### 👨‍⚕️ Custom Permission Classes

#### Role-Based Permissions
```python
from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_doctor

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_patient

class IsAdminOrDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_doctor)
```

#### Object-Level Permissions
```python
class IsAppointmentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.patient == request.user or obj.doctor == request.user

class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsReviewOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.patient == request.user
```

#### Time-Based Permissions
```python
from datetime import datetime

class IsWithinBusinessHours(permissions.BasePermission):
    def has_permission(self, request, view):
        current_hour = datetime.now().hour
        return 9 <= current_hour <= 17  # Business hours 9 AM to 5 PM
```

#### Action-Based Permissions
```python
class CanManageAppointments(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.is_doctor or request.user.is_staff)

class CanManageReviews(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_patient
```

### 🔑 Permission Usage Examples

#### View-Level Permissions
```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class DoctorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDoctor]
    # ... rest of the viewset

class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAppointmentOwner]
    # ... rest of the viewset
```

#### Function-Level Permissions
```python
from rest_framework.decorators import permission_classes

@permission_classes([IsAuthenticated, IsDoctor])
def doctor_dashboard(request):
    # ... view logic

@permission_classes([IsAuthenticated, IsPatient])
def patient_appointments(request):
    # ... view logic
```

### 📝 Permission Best Practices
1. Always use the most restrictive permission that meets your requirements
2. Combine multiple permissions when needed using lists
3. Use object-level permissions for fine-grained access control
4. Test permissions thoroughly, especially custom ones
5. Document permission requirements in API documentation
6. Consider caching permission results for performance
7. Use permission classes in combination with authentication classes

## 📋 Prerequisites

### 💻 System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git
- PostgreSQL (for production)

### 🛠️ Development Tools
- Code editor (VS Code, PyCharm, etc.)
- Postman or similar API testing tool
- Git client

## 🚀 Installation

1. **📥 Clone the repository**:
```bash
git clone [repository-url]
cd [project-directory]
```

2. **🔧 Create and activate virtual environment**:
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on Unix or MacOS
source .venv/bin/activate
```

3. **📦 Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **⚙️ Environment Setup**:
Create a `.env` file in the project root with the following variables:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. **🗄️ Database Setup**:
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

6. **📁 Static Files**:
```bash
python manage.py collectstatic
```

7. **▶️ Run Development Server**:
```bash
python manage.py runserver
```

## 📁 Project Structure

```
├── appointments/         # Appointment management app
│   ├── models.py        # Appointment models
│   ├── views.py         # Appointment views
│   ├── urls.py          # Appointment URLs
│   └── serializers.py   # Appointment serializers
├── config/              # Project configuration
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── media/              # User uploaded files
├── model_ai/           # AI model integration
├── rating/             # Doctor rating system
├── register_user/      # User registration and management
├── static/             # Static files
└── manage.py           # Django management script
```

## 📚 API Documentation

The API documentation is available at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

### 🔌 Available Endpoints

#### 🔐 Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset/confirm/` - Confirm password reset

#### 👥 User Endpoints
- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update current user profile
- `GET /api/users/doctors/` - List all doctors
- `GET /api/users/patients/` - List all patients

#### 📅 Appointment Endpoints
- `GET /api/appointments/` - List all appointments
- `POST /api/appointments/` - Create new appointment
- `GET /api/appointments/{id}/` - Get appointment details
- `PUT /api/appointments/{id}/` - Update appointment
- `DELETE /api/appointments/{id}/` - Delete appointment
- `GET /api/appointments/doctor/{doctor_id}/` - Get doctor's appointments
- `GET /api/appointments/patient/{patient_id}/` - Get patient's appointments
- `PUT /api/appointments/{id}/status/` - Update appointment status
- `GET /api/appointments/available-slots/` - Get available time slots

#### ⭐ Rating Endpoints
- `GET /api/ratings/` - List all ratings
- `POST /api/ratings/` - Create new rating
- `GET /api/ratings/{id}/` - Get rating details
- `PUT /api/ratings/{id}/` - Update rating
- `DELETE /api/ratings/{id}/` - Delete rating
- `GET /api/ratings/doctor/{doctor_id}/` - Get doctor's ratings
- `GET /api/ratings/patient/{patient_id}/` - Get patient's ratings

#### 📋 Specialization Endpoints
- `GET /api/specializations/` - List all specializations
- `POST /api/specializations/` - Create new specialization
- `GET /api/specializations/{id}/` - Get specialization details
- `PUT /api/specializations/{id}/` - Update specialization
- `DELETE /api/specializations/{id}/` - Delete specialization

#### 📊 Doctor Availability Endpoints
- `GET /api/availability/` - List all availability slots
- `POST /api/availability/` - Create new availability slot
- `GET /api/availability/{id}/` - Get availability details
- `PUT /api/availability/{id}/` - Update availability
- `DELETE /api/availability/{id}/` - Delete availability
- `GET /api/availability/doctor/{doctor_id}/` - Get doctor's availability

#### 💳 Payment Endpoints
- `POST /api/payments/` - Create new payment
- `GET /api/payments/{id}/` - Get payment details
- `GET /api/payments/appointment/{appointment_id}/` - Get appointment payment
- `POST /api/payments/verify/` - Verify payment
- `GET /api/payments/history/` - Get payment history

## 💻 Development

### 📝 Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions and classes

### 🧪 Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test appointments
```

### 🔄 Git Workflow
1. Create feature branch
2. Make changes
3. Write tests
4. Run tests
5. Create pull request

## 🚀 Deployment

### ✅ Production Checklist
- [ ] Set DEBUG=False
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure email settings
- [ ] Set up SSL certificate
- [ ] Configure backup system
- [ ] Set up monitoring

### 📋 Deployment Steps
1. Update environment variables
2. Run migrations
3. Collect static files
4. Configure web server
5. Set up SSL
6. Configure backup

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📝 Pull Request Process
1. Update documentation
2. Add tests if needed
3. Ensure all tests pass
4. Update the README.md if needed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For any queries or support, please contact:
- 📧 Email: [karimsalim33000@gmail.com](mailto:karimsalim33000@gmail.com)
- 💻 GitHub: [@karisalim](https://github.com/karisalim)
- 🔗 LinkedIn: [Karim Ahmed](https://www.linkedin.com/in/karim--salim/)
- 🐦 X (Twitter): [@KarimSalim4k](https://x.com/KarimSalim4k)

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- Material Design
- All contributors 
