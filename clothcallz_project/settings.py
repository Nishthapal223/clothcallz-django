from pathlib import Path
import os  # 👈 Added so we can use os.path for flexibility

# 📂 Base directory of your project
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Always keep your secret key safe
SECRET_KEY = 'django-insecure-change-this-to-a-strong-key'

# ✅ Debug mode ON for development (Turn OFF in production)
DEBUG = True

# 🌍 Allowed hosts (use '*' in development if needed)
ALLOWED_HOSTS = []

# 📦 Installed Django & third-party apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'store',                # Your shopping app

    # Third-party apps
    'crispy_forms',         # For better form styling
    'crispy_bootstrap5',    # Bootstrap 5 support for crispy forms
    'rest_framework',       # For API
]

# 🎨 Crispy Forms settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# 🛡 Middleware for security and session management
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🌐 Main URL configuration
ROOT_URLCONF = 'clothcallz_project.urls'

# 🎨 Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 👇 Now pointing to a 'templates' folder inside BASE_DIR
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🚀 WSGI application
WSGI_APPLICATION = 'clothcallz_project.wsgi.application'

# 💾 Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔑 No password validators for now (good for testing)
AUTH_PASSWORD_VALIDATORS = []

# 🌎 Language and timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 📂 Static files (CSS, JS, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # ✅ Your static folder
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # For production

# 📂 Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 🔑 Auto ID field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 💳 Razorpay keys (replace with real keys)
RAZORPAY_KEY_ID = "rzp_test_your_key"
RAZORPAY_KEY_SECRET = "your_secret_key"
