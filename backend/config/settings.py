import os
from pathlib import Path
import dj_database_url  # added for DATABASES config
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 환경 변수로 SECRET_KEY 관리
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-12345')

# 환경 변수로 DEBUG 제어 (프로덕션에서는 False)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# 환경 변수로 허용 호스트 관리
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    # Third party apps
    # 'rest_framework',
    'corsheaders',
    
    # Local apps
    'trades',
    'portfolios',
    'analysis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# 프로덕션에서는 PostgreSQL, 개발에서는 SQLite
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# React 빌드 파일 경로 (있으면 포함)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'frontend', 'build', 'static'),
] if os.path.exists(os.path.join(BASE_DIR, '..', 'frontend', 'build')) else []

# 미디어 파일 (차트 이미지 등)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# CORS settings
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        'https://bigsignal.web.app',
        'https://bigsignal.firebaseapp.com',
    ]

# CORS_ALLOW_CREDENTIALS = True

# Telegram settings
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID', '')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH', '')
TELEGRAM_PHONE = os.getenv('TELEGRAM_PHONE', '')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '')

# BigSignal specific settings
INITIAL_PORTFOLIO_BUDGET = 1000000  # 100만원
PORTFOLIO_CONFIGS = [
    {'name': 'BTC_Only', 'assets': ['BTC']},
    {'name': 'USDT_Only', 'assets': ['USDT']},
    {'name': 'DOGE_Only', 'assets': ['DOGE']},
    {'name': 'BTC_USDT', 'assets': ['BTC', 'USDT']},
    {'name': 'BTC_DOGE', 'assets': ['BTC', 'DOGE']},
    {'name': 'USDT_DOGE', 'assets': ['USDT', 'DOGE']},
    {'name': 'BTC_USDT_DOGE', 'assets': ['BTC', 'USDT', 'DOGE']},
]
SUPPORTED_ASSETS = ['BTC', 'USDT', 'DOGE']


# 프로덕션 보안 설정
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Whitenoise 정적 파일 압축
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS (프로덕션용)
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://bigsignal.web.app",  # Firebase 도메인
        "https://bigsignal.firebaseapp.com",
        "https://bigsignal-xxxxx.web.app",  # Firebase가 생성한 실제 도메인
    ]
    
    # Render 백엔드도 허용 (AJAX 요청용)
    CSRF_TRUSTED_ORIGINS = [
        "https://bigsignal-backend.onrender.com",
    ]