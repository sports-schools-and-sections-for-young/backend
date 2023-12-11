from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from sections.models import Section, SportType
from users.models import CustomUser

from .filters import SearchSectionFilter, SportTypeFilter
from .serializers import (CustomSerializers, SearchSectionSerializer,
                          SportTypeCreateSerializer,
                          SportTypeSerializer, RegisterSerializer)


class SearchSectionViewSet(ModelViewSet):
    """Вьюсет для поиска секций."""
    http_method_names = ('get', )
    queryset = Section.objects.all()
    serializer_class = SearchSectionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SearchSectionFilter


class SportTypeViewSet(ModelViewSet):
    """Вьюсет для отображения всех видов спорта."""
    http_method_names = ('get', )
    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SportTypeFilter


class SportTypeCreateViewSet(ModelViewSet):
    """Вьюсет для добавления вида спорта."""
    http_method_names = ('post', )
    queryset = SportType.objects.all()
    serializer_class = SportTypeCreateSerializer
    permission_classes = (IsAuthenticated, )


class RegisterViewSet(ModelViewSet):
    """Вьюсет для регистрации."""
    http_method_names = ('post',)
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class CustomAutenticateToken(APIView):
    serializer_class = CustomSerializers
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request)
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email, password=password)
            print(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        except serializers.ValidationError:
            ('Пользователь не найден')
