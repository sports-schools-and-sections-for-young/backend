import uuid

from djoser.serializers import UserSerializer
from haversine import haversine
from organizations.models import SportOrganization
from rest_framework import serializers
from sections.models import DayOfWeek, Section, SportType
from users.models import CustomUser


class SearchSectionSerializer(serializers.ModelSerializer):
    """Сериализатор для поиска секций."""
    sport_organization = serializers.CharField(
        source='sport_organization.title'
    )
    sport_type = serializers.CharField(source='sport_type.title')
    site = serializers.CharField(source='sport_organization.site')
    age_group = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    phone = serializers.CharField(source='sport_organization.phone')
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Section
        exclude = ('year_from', 'year_until')

    # Отображение возрастной группы
    def get_age_group(self, obj):
        return {
            "year_from": obj.year_from,
            "year_until": obj.year_until,
        }

    # Отображение дней работы секции
    def get_schedule(self, obj):
        schedule = ', '.join([day.title for day in obj.schedule.all()])
        if schedule:
            return schedule

    # Отображение расстояния от пользователя до секции
    def get_distance(self, obj):
        # Координаты по-умолчанию None, чтобы эндпойнт не сломался, если
        # координаты не были переданы
        coords = self.context.get('request').query_params.get('coords', None)
        if coords:
            # Получение широты и долготы пользователя
            user_lat, user_lon = map(float, coords.split(':'))
            # Координаты пользователя
            user_coords = (user_lat, user_lon)
            # Получение широты и долготы секции
            section_lat = obj.latitude
            section_lon = obj.longitude
            # Координаты секции
            section_coords = (section_lat, section_lon)
            # Расчет расстояния
            distance = haversine(user_coords, section_coords)
            return round(distance, 2)


class SportTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения всех видов спорта."""

    class Meta:
        model = SportType
        fields = '__all__'


class SportTypeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления вида спорта."""
    title = serializers.CharField()

    class Meta:
        model = SportType
        fields = '__all__'

    # Метод для добавления вида спорта
    def create(self, validated_data):
        title_data = validated_data.pop('title')
        first_word = title_data.split()[0]
        if not first_word.istitle():
            raise serializers.ValidationError(
                {'message':
                 'Название вида спорта должно начинаться с заглавной буквы!'}
            )
        if not title_data.replace(' ', '').isalpha():
            raise serializers.ValidationError(
                {'message':
                 'Название вида спорта должно содержать только буквы!'}
            )
        if SportType.objects.filter(title__iexact=title_data).exists():
            raise serializers.ValidationError(
                {'message': 'Такой вид спорта уже существует!'}
            )
        return SportType.objects.create(title=title_data)


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    password = serializers.CharField(write_only=True)
    check_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'check_password')

    # Метод для добавления пользователя
    def create(self, validated_data):
        password = validated_data.pop('password')
        check_password = validated_data.pop('check_password')
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        uuid = str(uuid.uuid4().hex[:12])
        if not username:
            validated_data['username'] = uuid
        if not first_name:
            validated_data['first_name'] = uuid
        if not last_name:
            validated_data['last_name'] = uuid
        if password == check_password:
            user = CustomUser.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user
        raise serializers.ValidationError(
            {'message': 'Пароли должны совпадать!'}
        )


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    class Meta:
        model = CustomUser
        fields = '__all__'


class SportOrganizationCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления спортшколы."""
    user = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = SportOrganization
        fields = '__all__'

    # Проверка существования спортшколы в базе
    def validate(self, data):
        user = self.context['request'].user
        if SportOrganization.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                {'message':
                 'У пользователя может быть только одна спортшкола.'}
            )
        return data


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра всех секции пользователя в профиле."""

    class Meta:
        model = Section
        fields = '__all__'


class SportOrganizationUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования спортшколы."""

    class Meta:
        model = SportOrganization
        exclude = ('user', )


class SectionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления секции спортшколы."""
    schedule = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DayOfWeek.objects.all()
    )

    class Meta:
        model = Section
        exclude = ('sport_organization', )

    # Метод для добавления секции спортшколы
    def create(self, validated_data):
        user = self.context['request'].user
        sport_organization_data = SportOrganization.objects.get(user=user)
        title_data = validated_data.pop('title')
        first_word = title_data.split()[0]
        if not first_word.istitle():
            raise serializers.ValidationError(
                {'message':
                 'Название секции должно начинаться с заглавной буквы!'}
            )
        if not title_data.replace(' ', '').isalpha():
            raise serializers.ValidationError(
                {'message': 'Название секции должно содержать только буквы!'}
            )
        schedule_data = validated_data.pop('schedule')
        section = Section.objects.create(
            sport_organization=sport_organization_data,
            title=title_data,
            **validated_data
        )
        section.schedule.set(schedule_data)
        return section

    # Проверка корректности ввода возраста
    def validate(self, data):
        if data['year_from'] > data['year_until']:
            raise serializers.ValidationError(
                {'message': 'Возрастная группа задана неверно'}
            )
        return data

    # Проверка существования секции в базе
    def validate_title(self, title):
        if Section.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                {'message': f'Секция с таким именем {title} уже существует'}
            )
        return title

    # Проверка стоимости занятия
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError(
                {'message': 'Цена должна быть положительным числом'}
            )
        return price


class SectionUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования секции спортшколы."""

    class Meta:
        model = Section
        fields = '__all__'


class SectionDeleteSerializer(serializers.ModelSerializer):
    """Сериализатор для удаления секции спортшколы."""

    class Meta:
        model = Section
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для личного кабинета организации спортивной школы."""

    class Meta:
        model = SportOrganization
        exclude = ('user', )
