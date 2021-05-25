"""local_mingle_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from utils.routers import DefaultRouter
from django.views.generic import TemplateView
from django.conf.urls import url
router = DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/events/', include('event.urls')),
    path('api/accounts/', include('rest_auth.urls')),
    path('api/profile/', include('accounts.urls')),
    path('api/payment/', include('payment.urls')),
    path('api/registrations/', include('rest_auth.registration.urls')),
    path('api/auth/', include('rest_social_auth.urls_token')),
    path('', TemplateView.as_view(template_name="index.html")),
    path('login/', TemplateView.as_view(template_name="account/user-login.html")),
    path('register/', TemplateView.as_view(template_name="account/user-register.html")),
    path('forgot-password/', TemplateView.as_view(template_name="account/forgot-password.html")),
    path('profile/', TemplateView.as_view(template_name="account/user-profile.html")),
    path('update-profile/', TemplateView.as_view(template_name="account/update_profile.html")),
    path('password-reset/', TemplateView.as_view(template_name="registration/password_reset_form.html")),
    path('password-reset-done/', TemplateView.as_view(template_name="registration/password_reset_done.html")),
    path('password-reset-complete/', TemplateView.as_view(template_name="registration/password_reset_complete.html")),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', TemplateView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]

admin.site.site_title = "Local Mingle"
admin.site.site_header = "Local Mingle Admin"
admin.site.index_title = "Welcome to Local Mingle Admin Portal"
