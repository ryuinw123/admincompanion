from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('test/', views.testEndPoint, name='test'),
    path('marker/', views.MarkerListView.as_view(), name="list_marker"),
    path('event/', views.EventListView.as_view(), name="list_event"),
    path('marker/<int:id>', views.ShowMarkerDetail.as_view(), name="marker_detail"),
    path('event/<int:id>', views.ShowEventDetail.as_view(), name="event_detail"),
    path('editMarker/<int:pk>',
         views.MarkerUpdateView.as_view(), name="marker_update"),
    path('editEvent/<int:pk>', views.EventUpdateView.as_view(), name="event_update"),
    path('uploadImages/', views.ImageUploadView.as_view(), name="image_create"),
    path('uploadImagesEvent/', views.ImageEventUploadView.as_view(),
         name="image_event_create"),
    path('report/', views.ReportListView.as_view(), name='report'),
    path('destroyComment/<int:comment_id>/',
         views.CommentDestroyAPIView.as_view(), name='comment_destroy'),
    path('destroyImage/<int:image_id>/',
         views.ImageDestroyAPIView.as_view(), name='image_destroy'),
    path('destroyImageEvent/<int:image_id>/',
         views.ImageEventDestroyAPIView.as_view(), name='event_destroy'),
    path('', views.getRoutes)
]
