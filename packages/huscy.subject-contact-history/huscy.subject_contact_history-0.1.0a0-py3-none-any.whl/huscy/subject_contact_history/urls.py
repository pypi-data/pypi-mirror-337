from django.urls import include, path
from rest_framework.routers import DefaultRouter

from huscy.subject_contact_history import views


router = DefaultRouter()
router.register('contacthistories', views.ContactHistoryViewSet, basename='contacthistory')

urlpatterns = [
    path('api/', include(router.urls)),
]
