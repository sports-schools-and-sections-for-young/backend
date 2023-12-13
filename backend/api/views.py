from django_filters.rest_framework import DjangoFilterBackend
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


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        if CustomUser.objects.filter(email=email).exists():
            return Response({'message': 'Пользователь с такими данными '
                            'существует.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomAuthenticationToken(APIView):
    serializer_class = CustomSerializers
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_authenticated:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key},
                                status=status.HTTP_200_OK)
            return Response({'message': 'Неверные данные'},
                            status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            ('Пользователь не найден')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAPIView(APIView):
    serializer_class = CustomSerializers

    def delete(self, request):
        serializer = CustomSerializers(request.user)
        del serializer
        return Response(status=status.HTTP_204_NO_CONTENT)
