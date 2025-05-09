from django.shortcuts import render
from .models import Movie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as status_code
from .management import MovieManagement
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import FileResponse, HttpResponse

class MovieListHandler(APIView):
    """
    View for movie lists
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status = status_code.HTTP_200_OK
        response = {}
        error = None

        movie_mgmt = MovieManagement()
        try:
            page = int(request.GET.get('page'))
        except Exception as e:
            page = 1
        response, error = movie_mgmt.get_movie_list(page)

        if error:
            #TODO: Create proper status codes based on errors
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response, status=status)
    
    def post(self, request):
        status = status_code.HTTP_200_OK
        response = {}
        error = None

        movie_mgmt = MovieManagement()
        video_name = request.data['video_name'] or None
        description = request.data['description'] or None
        video_file = request.data['video_file']
        try:
            thumbnail = request.data['thumbnail']
        except:
            thumbnail = None

        response, error = movie_mgmt.upload_new_movie(video_file, description, video_name, thumbnail)

        if error:
            #TODO: Create proper status codes based on errors
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response, status=status)

class MoviesHandler(APIView):
    """
    View for the movies request
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        status = status_code.HTTP_200_OK
        response = {}
        error = None

        movie_mgmt = MovieManagement()
        movie_id = id
        response, error = movie_mgmt.get_movie_details(movie_id)

        if error:
            #TODO: Create proper status codes based on errors
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response, status=status)

    def put(self, request, id):
        status = status_code.HTTP_200_OK
        response = {}
        error = None

        movie_mgmt = MovieManagement()
        video_name = request.data['video_name'] or None
        description = request.data['description'] or None
        video_file = request.data['video_file']
        try:
            thumbnail = request.data['thumbnail']
        except:
            thumbnail = None

        response, error = movie_mgmt.update_movie_details(id, video_file, description, video_name, thumbnail)
        if error:
            #TODO: Create proper status codes based on errors
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response, status=status)

    def delete(self, request, id):
        pass

class VideosHandler(APIView):
    """
    View for getting videos
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        status = status_code.HTTP_200_OK
        response = {}
        error = None

        movie_mgmt = MovieManagement()
        movie_id = id
        response, error = movie_mgmt.get_movie_video(movie_id)
        if error:
            #TODO: Create proper status codes based on errors
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR

        video_path = response['video']
        content_type = response['content_type']
        video_file = open(video_path, 'rb')
        return FileResponse(video_file, content_type=content_type, status=status)

        # return Response(false, status=500)

class ThumbnailHandler(APIView):
    """
    View for getting thumbnails
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        status = status_code.HTTP_200_OK
        response = {}
        error = None

        movie_mgmt = MovieManagement()
        response, error = movie_mgmt.get_movie_thumbnail(id)
        if error:
            #TODO: Create proper status codes based on errors
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR

        thumbnail_path = response['image']
        content_type = response['content_type']
        thumbnail_file = open(thumbnail_path, 'rb')
        return FileResponse(thumbnail_file, status=status)
