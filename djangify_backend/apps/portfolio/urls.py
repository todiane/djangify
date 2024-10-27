from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djangify_backend.apps.portfolio.views import (
    TechnologyViewSet,
    ProjectViewSet
)

router = DefaultRouter()
router.register(r'technologies', TechnologyViewSet, basename='technology')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
] 
