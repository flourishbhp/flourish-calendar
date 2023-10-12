import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_NAME = 'flourish_calendar'

DEBUG = True

DEVICE_ID = 4

DEVICE_ROLE = 'Client'

SECRET_KEY = 'secret'

DEFAULT_STUDY_SITE = 'site1'

ALLOWED_HOSTS = ['localhost']

SITE_ID = 1

BASE_FORMAT = '%Y-%m-%d'

ETC_DIR = os.path.join(BASE_DIR, APP_NAME)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_crypto_fields.apps.AppConfig',
    'edc_action_item.apps.AppConfig',
    'edc_calendar.apps.AppConfig',
    'edc_device.apps.AppConfig',
    'edc_lab.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'flourish.apps.AppConfig',
    'flourish.apps.EdcAppointmentAppConfig',
    'flourish.apps.EdcBaseAppConfig',
    'flourish.apps.EdcDataManagerAppConfig',
    'flourish.apps.EdcFacilityAppConfig',
    'flourish.apps.EdcLocatorAppConfig',
    'flourish.apps.EdcMetadataAppConfig',
    'flourish.apps.EdcOdkAppConfig',
    'flourish.apps.EdcProtocolAppConfig',
    'flourish.apps.EdcSenaiteInterfaceAppConfig',
    'flourish.apps.EdcTimepointAppConfig',
    'flourish.apps.EdcVisitTrackingAppConfig',
    'flourish_caregiver.apps.AppConfig',
    'flourish_child.apps.AppConfig',
    'flourish_follow.apps.AppConfig',
    'flourish_prn.apps.AppConfig',
    'pre_flourish.apps.AppConfig',
    'pre_flourish_follow.apps.AppConfig',
    'flourish_calendar.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'edc_dashboard.middleware.DashboardMiddleware',
    'edc_subject_dashboard.middleware.DashboardMiddleware',

]

ROOT_URLCONF = 'flourish_calendar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'flourish_calendar.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
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

DASHBOARD_URL_NAMES = {
    'subject_dashboard_url': 'flourish_dashboard:subject_dashboard_url',
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

COUNTRY = 'botswana'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
