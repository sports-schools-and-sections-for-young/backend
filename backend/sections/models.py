from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from organizations.models import Address, PhoneNumber, SportOrganization


class SportType(models.Model):
    """Модель вида спорта."""
    title = models.CharField(
        verbose_name='Название вида спорта',
        max_length=255,
        blank=False
    )

    class Meta:
        verbose_name = "Название вида спорта"
        verbose_name_plural = "Название видов спорта"
        ordering = ('id', )

    def __str__(self):
        return self.title


class AgeGroup(models.Model):
    """Модель возрастной группы."""
    year_from = models.PositiveIntegerField(
        verbose_name='Нижняя граница возрастной группы',
        validators=[
            MinLengthValidator(1, message='Минимум 1 символ'),
            MaxLengthValidator(2, message='Максимум 2 символа'),
        ],
        blank=False
    )
    year_until = models.PositiveIntegerField(
        verbose_name='Верхняя граница возрастной группы',
        validators=[
            MinLengthValidator(1, message='Минимум 1 символ'),
            MaxLengthValidator(2, message='Максимум 2 символа'),
        ],
        blank=False
    )

    class Meta:
        verbose_name = "Возрастная группа"
        verbose_name_plural = "Возрастные группы"
        ordering = ('id', )

    def __str__(self):
        return f'С {self.year_from} до {self.year_until} лет'


class Section(models.Model):
    """Модель секции."""
    sport_organization = models.ForeignKey(
        SportOrganization,
        verbose_name='Спортивная школа',
        on_delete=models.CASCADE,
        blank=False
    )
    title = models.CharField(
        verbose_name='Название секции',
        max_length=255,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=False
    )
    gender = models.CharField(
        verbose_name='Пол детей',
        max_length=7,
        blank=True
    )
    sport_type = models.ForeignKey(
        SportType,
        verbose_name='Вид спорта',
        on_delete=models.CASCADE,
        blank=False
    )
    age_group = models.ForeignKey(
        AgeGroup,
        verbose_name='Возрастная группа',
        on_delete=models.CASCADE,
        blank=False
    )
    address = models.ForeignKey(
        Address,
        verbose_name='Адрес секции',
        on_delete=models.CASCADE,
        blank=False
    )
    aviable = models.PositiveIntegerField(
        verbose_name='Наличие свободных мест',
        validators=[
            MinLengthValidator(1, message='Минимум 1 символ'),
            MaxLengthValidator(3, message='Максимум 3 символа'),
        ],
        null=True,
        blank=False,
        default=0
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоимость посещения секции в месяц в рублях',
        validators=[
            MinLengthValidator(1, message='Минимум 1 символ'),
            MaxLengthValidator(6, message='Максимум 6 символов'),
        ],
        null=True,
        blank=False,
        default=0
    )

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'
        ordering = ('sport_organization', 'title', )


class Trainer(models.Model):
    """Модель для тренера."""
    fio = models.CharField(
        verbose_name='Фамилия Имя Отчество',
        max_length=255,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=False
    )
    info = models.TextField(
        verbose_name='Информация о тренере',
        max_length=10000,
        blank=True
    )
    photo = models.ImageField(
        verbose_name='Фотография тренера',
        upload_to='img/trainers',
        blank=False
    )

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренера'
        ordering = ('id', )

    def __str__(self):
        return self.fio


class SectionTrainer(models.Model):
    """Модель, которая связывает секции и тренера."""
    section = models.ForeignKey(
        Section,
        verbose_name='Секция',
        on_delete=models.CASCADE,
        blank=False
    )
    trainer = models.ForeignKey(
        Trainer,
        verbose_name='Тренер',
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        verbose_name = "Секция и тренер"
        verbose_name_plural = "Секции и тренера"
        ordering = ('id', )


class DayOfWeek(models.Model):
    """Модель дня недели."""
    title = models.CharField(
        verbose_name='День недели',
        max_length=11,
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов')
        ],
        blank=False
    )

    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'
        ordering = ('id', )

    def __str__(self):
        return self.title


class Shedule(models.Model):
    """Модель расписания."""
    section = models.ForeignKey(
        Section,
        verbose_name='Секция',
        on_delete=models.CASCADE,
        blank=False
    )
    day = models.ForeignKey(
        DayOfWeek,
        verbose_name='День недели',
        on_delete=models.CASCADE,
        blank=False
    )
    time_from = models.TimeField(
        verbose_name='Время начала',
        blank=False
    )
    time_until = models.TimeField(
        verbose_name='Время окончания',
        blank=False
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ('id', )


class PhoneOfSection(models.Model):
    """Модель, которая связывает номера телефона и секцию спортшколы."""
    phone = models.ForeignKey(
        PhoneNumber,
        verbose_name='Номер телефона',
        on_delete=models.CASCADE,
        blank=False
    )
    section = models.ForeignKey(
        Section,
        verbose_name='Секция спортивной школы',
        on_delete=models.CASCADE,
        blank=False
    )


class PhotoOfSection(models.Model):
    """Модель фотографии секции."""
    photo = models.ImageField(
        verbose_name='Фотография секции',
        upload_to='img/sections',
        blank=True
    )
    section = models.ForeignKey(
        Section,
        verbose_name='Секция',
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ('id', )
