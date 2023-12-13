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
    # phone = serializers.SerializerMethodField()
    # comment = serializers.SerializerMethodField()
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

    # Получение телефона секции
    # def phone_of_section(self, obj):
    #     return PhoneOfSection.objects.filter(section=obj).first()

    # Отображение телефона секции
    # def get_phone(self, obj):
    #     return self.phone_of_section(obj).phone.value

    # Отображение комментария к телефону секции
    # def get_comment(self, obj):
    #     comment = self.phone_of_section(obj).phone.comment
    #     if comment:
    #         return comment

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
            section_lat = obj.address.latitude
            section_lon = obj.address.longitude
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
    check_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'check_password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        check_password = validated_data.pop('check_password')
        if password == check_password:
            user = CustomUser.objects.create(**validated_data,
                                             password=password)
            user.set_password('password')
            user.save()
            return user
        raise serializers.ValidationError('Пароли должны совпадать!')


class CustomUserSerializers(serializers.ModelSerializer):
    """Сериализатор для кастомного пользователя."""
    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class SportOrganizationCreateSerializers(serializers.ModelSerializer):
    """Сериализатор для добавления спортшколы."""
    user = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = SportOrganization
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        if SportOrganization.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                {'message':
                 'У пользователя может быть только одна спортшкола.'}
            )
        return data


class SectionCreateSerializers(serializers.ModelSerializer):
    """Сериализатор для добавления секции спортшколы."""
    # sport_organization = serializers.PrimaryKeyRelatedField(
    #     queryset=SportOrganization.objects.all()
    # )
    schedule = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DayOfWeek.objects.all()
    )

    class Meta:
        model = Section
        fields = (
            'id',
            # 'sport_organization',
            'title',
            'gender',
            'sport_type',
            'schedule',
            'price',
            'address',
            'year_from',
            'year_until',
            'latitude',
            'longitude'
        )

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
        section_lat = 0
        section_lon = 0
        coords = self.context.get('request').query_params.get('coords', None)
        if coords:
            section_lat, section_lon = map(float, coords.split(':'))
        section = Section.objects.create(
            sport_organization=sport_organization_data,
            title=title_data,
            latitude=section_lat,
            longitude=section_lon,
            **validated_data
        )
        section.schedule.set(schedule_data)
        return section

    def validate(self, data):
        if data['year_from'] > data['year_until']:
            raise serializers.ValidationError(
                {'message': 'Возрастная группа задана неверно'}
            )
        return data

    # Проверка схожесть наименований секций
    def validate_title(self, title):
        if Section.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                {'message': f'Секция с таким именем {title} уже существует'}
            )
        return title

    # Проверка положительного значения цены
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError(
                {'message': 'Цена должна быть положительным числом'}
            )
        return price


class SectionDeleteSerializer(serializers.ModelSerializer):
    """Сериализатор для удаления секции спортшколы."""
    class Meta:
        model = Section
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для личного кабинета организации спортивной школы."""
    class Meta:
        model = SportOrganization
        fields = ('id', 'title', 'address')
