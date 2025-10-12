from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- GÜVENLİK ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'yerel-gelistirme-icin-guvensiz-anahtar')
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Kendi sitenizin adını da manuel olarak ekleyerek garantileyin
ALLOWED_HOSTS.append('doktor-nobet-sistemi.onrender.com')

# --- UYGULAMALAR ---
INSTALLED_APPS = [ 'core.apps.CoreConfig', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'whitenoise.runserver_nostatic', 'django.contrib.staticfiles' ]
MIDDLEWARE = [ 'django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware' ]
ROOT_URLCONF = 'nobet_sistemi.urls'
TEMPLATES = [ { 'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': { 'context_processors': [ 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages' ], }, }, ]
WSGI_APPLICATION = 'nobet_sistemi.wsgi.application'

# --- VERİTABANI ---
DATABASES = { 'default': dj_database_url.config( default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600 ) }

# --- DİL & ZAMAN ---
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# --- STATİK DOSYALAR ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- YÖNLENDİRME ---
LOGIN_REDIRECT_URL = 'doktor_paneli_redirect'
LOGOUT_REDIRECT_URL = 'login'

# --- YENİ EKLENECEK SATIR ---
# Django'ya bizim özel giriş sayfamızın 'login' olduğunu söyle.
LOGIN_URL = 'login'