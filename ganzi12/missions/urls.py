from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MissionViewSet, CompletedViewSet, CompletedListView

router = DefaultRouter()
router.register(r'', MissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:mission_id>/completed/', CompletedViewSet.as_view({'get': 'list', 'post': 'create'}), name='completed-mission'),
    path('completed/list', CompletedListView.as_view(), name='completed-list'),
]