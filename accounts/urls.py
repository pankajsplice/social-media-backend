import djoser.views
from django.conf.urls import url
from django.contrib.auth import get_user_model
from rest_framework import routers
from django.urls import path, include
router = routers.DefaultRouter()
User = get_user_model()

router.register(r'user_list', djoser.views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
