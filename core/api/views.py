from django.contrib.auth import authenticate
from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from .models import Music
from .serializers import MusicSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'username': user.username
            })
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            return Response({'error': 'Нужен и логин, и пароль'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': user},
                            status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Нужен refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error', 'Неверный refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Выход был успешно выполнен'}, status=status.HTTP_200_OK)

class ReadListView(APIView):
    def get(self, request):
        musics = Music.objects.all()
        serializer = MusicSerializer(musics, many=True)
        if musics.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error', 'Песни отсутствуют'}, status=status.HTTP_400_BAD_REQUEST)

class ReadDetailView(APIView):
    def get(self, request, pk):
        musics = Music.objects.filter(pk=pk)
        if musics.exists():
            serializer = MusicSerializer(musics)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": 'Псени по данному ID не было найдено'}, status=status.HTTP_404_NOT_FOUND)

class CreateView(APIView):
    def post(self, request):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def stream_file(path):
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            yield chunk

class StreamMusicAPIView(APIView):
    def get(self, request, pk):
        try:
            music = Music.objects.get(id=pk)
            response = StreamingHttpResponse(
                stream_file(Music.file.path),
                content_type='audio/mpeg'
            )
            response['Content-Disposition'] = f'inline; filename="{Music.file.name}"'
            return response
        except Music.DoesNotExist:
            return Response({'error': 'Track not found'}, status=status.HTTP_404_NOT_FOUND)

class DeleteView(APIView):
    def post(self, request, pk):
        musics = Music.object.filter(pk=pk)
        if musics.exists():
            music = musics.first()
            music.delete()
            return Response({'success': 'Вы успешно удалили песню'}, status=status.HTTP_200_OK)
        return Response({'error': 'Песни не найдено'})