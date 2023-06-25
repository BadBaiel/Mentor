from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from .models import Mentor
from .serializers import MentorSerializer, MentorDetailSerializer, MentorListsSerializer, MentorProfileSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MentorFilter
from django.db.models import Count
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.serializers import PersonalProfileSerializer
class MentorListAPIView(ListAPIView):
    queryset = Mentor.objects.filter(is_active=True).annotate(like_count=Count('likes')).order_by('-like_count')
    serializer_class = MentorListsSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MentorFilter


class MentorCreateAPIView(CreateAPIView):
    queryset = Mentor.objects.filter(is_active=True)
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        user = request.user  # Получаем текущего пользователя

        mentor_data = {
            'user': user.id,
            'directions': user.directions,
            'month': user.month,
            'group': request.data['group'],
            'name': request.data['name'],
            'contact': request.data['contact'],
            'about_me': request.data['about_me'],
            'skills': request.data['skills'],
            'employment': request.data['employment']
        }

        serializer = MentorSerializer(data=mentor_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    # def post(self, request, *args, **kwargs):
    #     serializer_class = MentorSerializer
    #     serializer_data = serializer_class.validated_data
    #     serializer_data['user'] = request.user.id
    #     serializer_class.save()


class MentorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.filter(is_active=True)
    serializer_class = MentorDetailSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class MentorProfileView(APIView):
    def get(self, request):
        user = request.user
        if user.is_mentor:
            snippets = Mentor.objects.filter(user=user)
            serializer = MentorProfileSerializer(snippets, many=True)
            return Response(serializer.data)
        else:
            snippets = User.objects.filter(email=user.email)
            serializer = PersonalProfileSerializer(snippets, many=True)
            return Response(serializer.data)

#    if Mentor.objects.filter(is_mentor=True):
#        serializer_class = MentorProfileSerializer
#
#        def get(self, request):
#            snippets = Mentor.objects.filter(user=request.user)
#            serializer = MentorProfileSerializer(snippets, many=True)
#
#            return Response(serializer.data)
#    else:
#
#        serializer_class = PersonalProfileSerializer
#
#        def get(self, request):
#                snippets = User.objects.filter(email=request.user)
#                serializer = PersonalProfileSerializer(snippets, many=True)
#
#                return Response(serializer.data)


class AddLike(ListCreateAPIView):
    def post(self, request, pk, *args, **kwargs):
        mentor = Mentor.objects.get(pk=pk)
        is_dislike = False

        for dislike in mentor.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            mentor.dislikes.remove(request.user)

        is_like = False

        for like in mentor.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            mentor.likes.add(request.user)

        if is_like:
            mentor.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddDislike(ListCreateAPIView):
    def post(self, request, pk, *args, **kwargs):
        mentor = Mentor.objects.get(pk=pk)
        is_like = False

        for like in mentor.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            mentor.likes.remove(request.user)

        is_dislike = False

        for dislike in mentor.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            mentor.dislikes.add(request.user)

        if is_dislike:
            mentor.dislikes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)








