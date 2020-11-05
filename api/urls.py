from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import SignupViewSet, SigninViewSet, TopicViewSet

router = DefaultRouter()
router.register(r'signup', SignupViewSet, basename='signup')
router.register(r'signin', SigninViewSet, basename='signin')
router.register(r'topic', TopicViewSet, basename='topic')

urlpatterns = router.urls