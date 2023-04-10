from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer, MarkerSerializer, EventSerializer, ImageSerializer, CommentSerializer, ImageEventSerializer,ReportMarkerSerializer , ReportEventSerializer , EventURLSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from api.models import Marker, Event, Image, Comment, ImageEvent, ReportEvent, ReportMarker , EventUrl
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.db import connection

# Create your views here.

# nextcloud
import nextcloud_client

nc = nextcloud_client.Client('http://nextcloud.shitduck.duckdns.org/')
nc.login('pokemon', 'Pokemon19!!')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MarkerListView(generics.ListAPIView):
    serializer_class = MarkerSerializer

    def get_queryset(self):
        queryset = Marker.objects.filter(
            permissionmarker__isnull=False).distinct()
        return queryset


class CommentDestroyAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    lookup_field = 'comment_id'


class ImageDestroyAPIView(generics.DestroyAPIView):
    queryset = Image.objects.all()
    lookup_field = 'image_id'


class ImageEventDestroyAPIView(generics.DestroyAPIView):
    queryset = ImageEvent.objects.all()
    lookup_field = 'image_id'


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.filter(enable=1)


class ReportListView(APIView):
    def get(self, request):
        markers = ReportMarker.objects.filter(enable=1).order_by('-created_time')
        events = ReportEvent.objects.filter(enable=1).order_by('-created_time')
        serialized_reports = []
        for marker in markers:
            serialized_reports.append(ReportMarkerSerializer(marker).data)
        for event in events:
            serialized_reports.append(ReportEventSerializer(event).data)
        sorted_reports = sorted(serialized_reports, key=lambda report: report['created_time'], reverse=True)
        return Response(sorted_reports)


class MarkerUpdateView(generics.UpdateAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def put(self, request, *args, **kwargs):
        marker_id = kwargs.get('pk')
        marker = self.get_object()
        serializer = self.get_serializer(marker, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def put(self, request, *args, **kwargs):
        event_id = kwargs.get('pk')
        event = self.get_object()
        print(request.data)
        serializer = self.get_serializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        eventtype = request.data.get('event_type')

        print("Eventtype = " , eventtype)

        if eventtype == '1':
            url = request.data.get('url')
            print("url = " , url)
            event_url, created = EventUrl.objects.get_or_create(event_url=event)
            event_url.url = url
            event_url.save()
        elif eventtype == '0':
            EventUrl.objects.filter(event_url=event).delete()

        return Response(serializer.data)


class ShowMarkerDetail(APIView):
    def get(self, request, id):
        marker_data = Marker.objects.filter(id=id).first()
        images_data = Image.objects.filter(marker=id)
        comments_data = Comment.objects.filter(comment_marker_id=id)
        serialized_marker = MarkerSerializer(marker_data).data
        serialized_image = ImageSerializer(images_data, many=True).data
        serialized_comments = CommentSerializer(comments_data, many=True).data
        data = {
            'marker': serialized_marker,
            'images': serialized_image,
            'comments': serialized_comments
        }
        return Response(data)


class ShowEventDetail(APIView):
    def get(self, request, id):
        event_data = Event.objects.filter(event_id=id).first()
        images_data = ImageEvent.objects.filter(event_id=id)
        eventUrl_data = EventUrl.objects.filter(event_url = id).first()
        
        serialized_event = EventSerializer(event_data).data
        serialized_image = ImageEventSerializer(images_data, many=True).data
        serialized_url = EventURLSerializer(eventUrl_data).data

        serialized_event.update(serialized_url)
        data = {
            'event': serialized_event,
            'images': serialized_image,
        }
        
        return Response(data)


class ImageUploadView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        marker_id = request.POST.get('marker_id')

        # Save the image to default storage
        path = default_storage.save(f'tmp/image.png', ContentFile(file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        # Upload the image to OwnCloud server
        index = kwargs.get('image_id', None)
        if index is None:
            index = Image.objects.latest('image_id').image_id + 1
        nc.put_file(f"KMITLcompanion/image{index}.png", tmp_file)
        link_info = nc.share_file_with_link(f'KMITLcompanion/image{index}.png')

        # Save the image data to the database
        image = Image.objects.create(
            marker_id=marker_id, link=f'{link_info.get_link()}/preview')
        serializer = self.get_serializer(image)

        os.remove(settings.MEDIA_ROOT + tmp_file)

        return Response(serializer.data)


class ImageEventUploadView(generics.CreateAPIView):
    queryset = ImageEvent.objects.all()
    serializer_class = ImageEventSerializer

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        event_id = request.POST.get('event_id')

        # Save the image to default storage
        path = default_storage.save(f'tmp/image.png', ContentFile(file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        # Upload the image to OwnCloud server
        index = kwargs.get('image_id', None)
        if index is None:
            index = ImageEvent.objects.latest('image_id').image_id + 1
        nc.put_file(f"KMITLcompanion/image{index}.png", tmp_file)
        link_info = nc.share_file_with_link(f'KMITLcompanion/image{index}.png')

        # Save the image data to the database
        image = ImageEvent.objects.create(
            event_id=event_id, link=f'{link_info.get_link()}/preview')
        serializer = self.get_serializer(image)

        os.remove(settings.MEDIA_ROOT + tmp_file)

        return Response(serializer.data)

class ReportMarkerUpdateAPIView(generics.UpdateAPIView):
    queryset = ReportMarker.objects.all()
    serializer_class = ReportMarkerSerializer

    def update(self, request, *args, **kwargs ,):
        report_marker_id = kwargs.get('report_marker_id')
        report_marker = ReportMarker.objects.get(report_marker_id=report_marker_id)
        report_marker.enable = 0
        report_marker.save()
        return Response(status=status.HTTP_200_OK)

class ReportEventUpdateAPIView(generics.UpdateAPIView):
    queryset = ReportEvent.objects.all()
    serializer_class = ReportEventSerializer

    def update(self, request, *args, **kwargs ,):
        report_event_id = kwargs.get('report_event_id')
        report_event_id = ReportEvent.objects.get(report_event_id=report_event_id)
        report_event_id.enable = 0
        report_event_id.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/token/refresh/',
        '/api/prediction/',
        '/api/marker/',
        '/api/event',
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"ยินดีต้อนรับ {request.user}"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)
