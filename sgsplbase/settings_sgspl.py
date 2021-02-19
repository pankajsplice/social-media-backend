REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'accounts.serializers.RegisterSerializer',
}
#
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.UserDetailsSerializer',
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# AUTH BACKEND
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


REST_SESSION_LOGIN = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

#custom
HTML_MINIFY = True
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']

CKEDITOR_UPLOAD_PATH = "uploads/"



#ckeditor
CKEDITOR_CONFIGS = {
    'default': {

        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            # {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'document', 'items': ['Source', '-', 'Save', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},

            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'uploadwidget', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},

            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},

            #
            # {'name': 'yourcustomtools', 'items': [
            #     # put the name of your editor.ui.addButton here
            #     'Preview',
            #     'Maximize',
            #
            # ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 291,
        'width': '100%',
        'filebrowserWindowHeight': 725,
        'filebrowserWindowWidth': 940,
        'toolbarCanCollapse': True,
        'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}


# EMAIL_HOST = 'in-v3.mailjet.com'
# EMAIL_PORT = '587'
# EMAIL_HOST_USER = 'bd83e39a4e19891beae6420600ccf6cc'
# EMAIL_HOST_PASSWORD = 'c1de3dc0846236370c9f51de0d935fb7'
# EMAIL_USE_TLS = True
#
# DEFAULT_FROM_EMAIL = 'support@spliceglobal.com'
# MM_AMDIN_EMAIL = 'support@spliceglobal.com'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#Email Staging credentials
EMAIL_FROM = 'info@easypon.com'
SENDER = EMAIL_FROM
SENDERNAME = 'EasyPon'
DEFAULT_FROM_EMAIL = EMAIL_FROM
EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAJ42VUSUWBQIVBJWA'
EMAIL_HOST_PASSWORD = 'Ar/MZuqDRoxSwXZAmpTK9GVXFZG+ONG5dpgVRfdAZsX5'

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
