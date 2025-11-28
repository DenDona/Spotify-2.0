app_name = 'api'
from django.urls import path
from .views import StreamMusicAPIView, CreateView, ReadDetailView, ReadListView

urlpatterns = [
    path('api/tracks/', ReadListView.as_view(), name='track-list'),
    path('api/stream/<int:track_id>/', StreamMusicAPIView.as_view(), name='stream-track'),
    path('api/tracks/create/', CreateView.as_view(), name='create-track'),
    path('api/tracks/<int:pk>/', ReadDetailView.as_view(), name='detail-track')
]