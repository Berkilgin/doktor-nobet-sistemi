from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- GÜVENLİK AYARLARI ---
# SECRET_KEY'i artık koddan değil, ortam değişkeninden alacağız.
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG modu, sadece yerelde çalışırken True, sunucuda False olmalı.
# Render.com, 'RENDER' adında bir ortam değişkeni otomatik olarak ayarlar.
DEBUG = 'RENDER' not in os.environ

# Sunucunun domain adını ve Render'ın kendi verdiği adresi buraya ekleyeceğiz.
ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# --- YENİ EKLENECEK SATIR ---
# Güvenlik için, manuel olarak da host adımızı ekleyelim.
ALLOWED_HOSTS.append('doktor-nobet-sistemi.onrender.com')

# --- UYGULAMA TANIMLARI ---
INSTALLED_APPS = [
    'core.apps.CoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # WhiteNoise entegrasyonu
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # WhiteNoise entegrasyonu
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nobet_sistemi.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'nobet_sistemi.wsgi.application'

# --- VERİTABANI AYARLARI ---
# Yerelde SQLite, sunucuda PostgreSQL kullanacağız.
DATABASES = {
    'default': dj_database_url.config(
        # Render'ın vereceği veritabanı URL'sini kullan, bulamazsan SQLite kullan.
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# --- DİL VE ZAMAN AYARLARI ---
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# --- STATİK DOSYA AYARLARI ---
STATIC_URL = 'static/'
# Sunucuda statik dosyaların toplanacağı yer
STATIC_ROOT = BASE_DIR / 'staticfiles'
# WhiteNoise için depolama ayarı
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- YÖNLENDİRME AYARLARI ---
LOGIN_REDIRECT_URL = 'doktor_paneli_redirect'
LOGOUT_REDIRECT_URL = 'login'