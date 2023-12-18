from django.contrib.auth import authenticate
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from organizations.models import SportOrganization
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from sections.models import Section, SportType
from users.models import CustomUser

from .filters import SearchSectionFilter, SportTypeFilter
from .pagination import CustomPageNumberPagination
from .serializers import (CustomUserSerializer, ProfileSerializer,
                          RegisterSerializer, SearchSectionSerializer,
                          SectionCreateSerializer, SectionDeleteSerializer,
                          SectionSerializer, SectionUpdateSerializer,
                          SportOrganizationCreateSerializer,
                          SportOrganizationUpdateSerializer,
                          SportTypeCreateSerializer, SportTypeSerializer)


class SearchSectionViewSet(ModelViewSet):
    """Вьюсет для поиска секций."""
    http_method_names = ('get', )
    queryset = Section.objects.all()
    serializer_class = SearchSectionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SearchSectionFilter
    pagination_class = CustomPageNumberPagination


class SportTypeAllViewSet(ModelViewSet):
    """Вьюсет для отображения всех видов спорта."""
    http_method_names = ('get', )
    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class SportTypeViewSet(ModelViewSet):
    """
    Вьюсет для отображения видов спорта, которые привязаны хотя бы к одной
    секции.
    """
    http_method_names = ('get', )
    queryset = SportType.objects.all()
    serializer_class = SportTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SportTypeFilter

    def get_queryset(self):
        queryset = SportType.objects.annotate(sections_count=Count('section'))
        queryset = queryset.filter(sections_count__gt=0)
        return queryset


class SportTypeCreateViewSet(ModelViewSet):
    """Вьюсет для добавления вида спорта."""
    http_method_names = ('post', )
    queryset = SportType.objects.all()
    serializer_class = SportTypeCreateSerializer
    permission_classes = (IsAuthenticated, )


class RegisterAPIView(APIView):
    """Вьюсет для регистрации пользователя."""
    http_method_names = ('post', )
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {'message': 'Пользователь с такими данными уже существует!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomAuthenticationToken(APIView):
    """Вьюсет для авторизации пользователя."""
    http_method_names = ('post', )
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},
                            status=status.HTTP_200_OK)
        return Response(
            {'message': 'Пользователь с такими данными не существует!'},
            status=status.HTTP_404_NOT_FOUND
        )


class ResetPasswordAPIView(APIView):
    """Вьюсет для смены пароля пользователя."""
    http_method_names = ('put', )
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, )

    def put(self, request):
        email = request.user.email
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        check_password = request.data.get('check_password')
        if new_password != check_password:
            return Response({'message': 'Пароли не совпадают!'},
                            status=status.HTTP_400_BAD_REQUEST)
        if old_password == new_password:
            return Response({'message': 'Старый и новый пароли не должны '
                             'совпадать!'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=old_password)
        if user:
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Пароль успешно изменен!'},
                            status=status.HTTP_200_OK)
        return Response(
            {'message': 'Пользователь с такими данными не существует!'},
            status=status.HTTP_404_NOT_FOUND
        )


class DeleteUserAPIView(APIView):
    """Вьюсет для удаления пользователя."""
    http_method_names = ('delete', )
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, )

    def delete(self, request):
        user = get_object_or_404(CustomUser, id=request.user.id)
        if user.is_authenticated:
            user.delete()
            return Response({'message': 'Пользователь успешно удален'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Пользователь не аутентифицирован'},
                        status=status.HTTP_401_UNAUTHORIZED)


class SportOrganizationCreateViewSet(ModelViewSet):
    """Вьюсет для добавления спортшколы."""
    http_method_names = ('post', )
    queryset = SportOrganization.objects.all()
    serializer_class = SportOrganizationCreateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)


class SportOrganizationUpdateViewSet(ModelViewSet):
    """Вьюсет для редактирования спортшколы."""
    http_method_names = ('patch', )
    queryset = SportOrganization.objects.all()
    serializer_class = SportOrganizationUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        try:
            id_sportschool = SportOrganization.objects.get(
                user=request.user
            ).id
            instance = SportOrganization.objects.get(id=id_sportschool)
            if instance.user != request.user:
                return Response(
                    {'message':
                     'У вас нет прав для редактирования этой спортивной '
                     'школы!'},
                    status=status.HTTP_403_FORBIDDEN)
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SportOrganization.DoesNotExist:
            return Response({'message': 'Спортивная школа не существует!'},
                            status=status.HTTP_404_NOT_FOUND)


class SectionAPIView(APIView):
    """Вьюсет для просмотра всех секции пользователя в профиле."""
    http_method_names = ('get', )
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        sections = Section.objects.filter(
            sport_organization__user=request.user
        )
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)


class SectionCreateViewSet(ModelViewSet):
    """Вьюсет для добавления секции спортшколы."""
    http_method_names = ('post', )
    queryset = Section.objects.all()
    serializer_class = SectionCreateSerializer
    permission_classes = (IsAuthenticated, )


class SectionUpdateViewSet(ModelViewSet):
    """Вьюсет для редактирования секции спортшколы."""
    http_method_names = ('patch', )
    queryset = Section.objects.all()
    serializer_class = SectionUpdateSerializer
    permission_classes = (IsAuthenticated, )


class SectionDeleteAPIView(APIView):
    """Вьюсет для удаления секции спортшколы."""
    http_method_names = ('delete', )
    queryset = Section.objects.all()
    serializer_class = SectionDeleteSerializer
    permission_classes = (IsAuthenticated, )

    def delete(self, request, id):
        try:
            section = self.queryset.get(id=id)
            if section.sport_organization.user != request.user:
                return Response(
                    {'message': 'У вас нет прав на удаление этой секции!'},
                    status=status.HTTP_403_FORBIDDEN
                )
            section.delete()
            return Response({'message': 'Секция успешно удалена.'},
                            status=status.HTTP_204_NO_CONTENT)
        except Section.DoesNotExist:
            return Response({'message': 'Секция не существует!'},
                            status=status.HTTP_404_NOT_FOUND)


class ProfileAPIView(APIView):
    """Вьюсет для отображения спортшколы в личном кабинете."""
    http_method_names = ('get', )
    queryset = SportOrganization.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            id_sportschool = SportOrganization.objects.get(
                user=request.user
            ).id
            profile = self.queryset.get(id=id_sportschool)
            if profile.user != request.user:
                return Response(
                    {'message':
                        'У вас нет прав для просмотра этой спортивной школы!'},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.serializer_class(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SportOrganization.DoesNotExist:
            return Response({'message': 'Спортивная школа не существует!'},
                            status=status.HTTP_404_NOT_FOUND)
