from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieListHandler.as_view(), name='movies'),
    path('<int:id>/', views.MoviesHandler.as_view(), name='movie_detail'),
    path('video/<int:id>', views.VideosHandler.as_view(), name="video"),
    path('thumbnail/<int:id>', views.ThumbnailHandler.as_view(), name="thumbnail"),
]