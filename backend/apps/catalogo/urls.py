from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BarbieViewSet, BarbieImageViewSet, StatisticsView, VisionAnalysisView

router = DefaultRouter()
router.register(r'barbies', BarbieViewSet)
router.register(r'images', BarbieImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('vision/analyze/', VisionAnalysisView.as_view(), name='vision_analyze'),
]
