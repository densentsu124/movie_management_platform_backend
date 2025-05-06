from .models import Movie
from django.core.paginator import Paginator
from .serializers import MovieSerializer
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import cv2
from PIL import Image
import os
from urllib.parse import unquote
from movie_management.settings import MEDIA_ROOT
from django.http import FileResponse

class MovieManagement:
    
    def __init__(self):
        self._model = Movie

    def get_movie_list(self, page:int=1):
        # Returns a list of Movie id, names, thumbnail
        movie_list = []
        error = None

        #TODO: Change this into something more optimized when scaling
        movie_list = Movie.objects.all()

        pagination = Paginator(movie_list, 20)
        if pagination.count:
            serializer = MovieSerializer(pagination.page(page).object_list, many=True)
            return (serializer.data, error)
        else:
            error = "NO DATA FOUND"
            return (None, error)

    def get_movie_details(self, movie_id):
        # Returns a specific movie's details
        error = None
        try:
            movie_instance = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return {'error' : 'Movie not found'}

        serializer = MovieSerializer(movie_instance)
        return (serializer.data, error)

    def get_movie_video(self, movie_id):
        # Returns movie video

        #TODO: Ideally there's a different server for serving the video like AWS
        error = None
        response = None
        try:
            movie_instance = Movie.objects.get(id=movie_id)

            serializer = MovieSerializer(movie_instance)
            base_name = os.path.basename(serializer.data['video_file'])
            filename, file_type = os.path.splitext(base_name)
            path = f'{MEDIA_ROOT}\\videos\\{unquote(filename)}{file_type}'
            response = {
                "video": path,
                "content_type": 'video/mp4'
            }
        except Movie.DoesNotExist:
            error = 'Movie not found'
        return (response, error)

    def get_movie_snippet(self, movie_id):
        # Returns movie snippet

        #TODO: This is currently the same as get_movie_video()
        try:
            movie_instance = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return {'error' : 'Movie not found'}

        serializer = MovieSerializer(movie_instance, fields=('video_file',))
        return serializer.data

    def get_movie_thumbnail(self, movie_id):
        # Returns a thumbnail

        #TODO: Ideally there's a different server for serving Images like AWS
        error = None
        response = None
        try:
            movie_instance = Movie.objects.get(id=movie_id)

            serializer = MovieSerializer(movie_instance)
            base_name = os.path.basename(serializer.data['thumbnail'])
            filename, file_type = os.path.splitext(base_name)
            path = f'{MEDIA_ROOT}\\thumbnails\\{unquote(filename)}{file_type}'
            response = {
                "image": path,
                "content_type": 'image/*'
            }
        except Movie.DoesNotExist:
            error = 'Movie not found'
        return (response, error)

    def upload_new_movie(self, video_file, description, video_name, thumbnail=None):
        error = None
        thumbnail_file_path = ""
        if video_file:

            video_file_name = default_storage.save(f'videos\\{video_name or video_file.name}.{video_file.content_type.split("/")[1]}', video_file)
            video_file_path = default_storage.path(video_file_name)

            if thumbnail:
                thumbnail_name = default_storage.save(f'thumbnails\\{video_name or thumbnail.name}.{thumbnail.content_type.split("/")[1]}', thumbnail)
                thumbnail_file_path = default_storage.path(thumbnail_name)
            else:
                try:
                    vidcap = cv2.VideoCapture(video_file_path)
                    success, image = vidcap.read()
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(image)
                    if success:
                        base_filename = os.path.basename(video_file_name)
                        thumbnail_name, _ = os.path.splitext(base_filename)
                        thumbnail_file_path = f'{default_storage.location}\\thumbnails\\{thumbnail_name}.jpg'
                        img.save(thumbnail_file_path)
                except Exception as e:
                    print(e)
                finally:
                    vidcap.release()

            movie = Movie(
                title=video_name,
                video_file=video_file_path,
                description=description,
                thumbnail=thumbnail_file_path,
            )
            serializer = MovieSerializer(movie)
            if serializer.is_valid:
                movie.save()

        else:
            error = "VIDEO FILE DOES NOT EXIST"
            return (None, error)
    
        return (True, error)

    def update_movie_details(self, movie_id, video_file=None, description=None, video_name=None, thumbnail=None):
        error = None
        thumbnail_file_path = ""

        movie_instance = Movie.objects.get(id=movie_id)
        if video_file:
            #TODO: Delete the old video file
            video_file_name = default_storage.save(f'videos\\{video_name or video_file.name}.{video_file.content_type.split("/")[1]}', video_file)
            video_file_path = default_storage.path(video_file_name)
            movie_instance.video_file = video_file_path

            if not thumbnail:
                try:
                    vidcap = cv2.VideoCapture(video_file_path)
                    success, image = vidcap.read()
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(image)
                    if success:
                        base_filename = os.path.basename(video_file_name)
                        thumbnail_name, _ = os.path.splitext(base_filename)
                        thumbnail_file_path = f'{default_storage.location}\\thumbnails\\{thumbnail_name}.jpg'
                        img.save(thumbnail_file_path)
                        movie_instance.thumbnail = thumbnail_file_path
                except Exception as e:
                    print(e)
                finally:
                    vidcap.release()

        #TODO: Delete the old thumbnail file
        if thumbnail:
            thumbnail_name = default_storage.save(f'thumbnails\\{video_name or thumbnail.name}.{thumbnail.content_type.split("/")[1]}', thumbnail)
            thumbnail_file_path = default_storage.path(thumbnail_name)
            movie_instance.thumbnail = thumbnail_file_path

        if description:
            movie_instance.description = description

        if video_name:
            movie_instance.title = video_name

        try:
            movie_instance.save()
        except:
            error = "UPDATING DATA FAILED"

        serializer = MovieSerializer(movie_instance)
        return (serializer.data, error)

    def delete_movie(self, movie_id):
        # DELETE Method... Returns true on success
        error = None
        try:
            movie_instance = Movie.objects.get(id=movie_id)
            movie_instance.delete()
            #TODO: Create a file deletion function to remove deleted videos/thumbnails

            return (None, error)
        except Movie.DoesNotExist:
            return (None, {'error' : 'Movie deletion failed'})
