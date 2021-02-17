# # Database
# # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
#
DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': 'ducisdb',
        'USER': 'postgres',
        'PASSWORD': '5VFonntogRuVvp4mvWC1',
        'HOST': 'ducisdb.cur4wfqjcdam.ap-south-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}
