# Generated by Django 3.2.3 on 2023-11-06 07:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_from', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное значение 1'), django.core.validators.MaxValueValidator(99, message='Максимальное значение 99')], verbose_name='Нижняя граница возрастной группы')),
                ('year_until', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное значение 1'), django.core.validators.MaxValueValidator(99, message='Максимальное значение 99')], verbose_name='Верхняя граница возрастной группы')),
            ],
            options={
                'verbose_name': 'Возрастная группа',
                'verbose_name_plural': 'Возрастные группы',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='DayOfWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='День недели')),
            ],
            options={
                'verbose_name': 'День недели',
                'verbose_name_plural': 'Дни недели',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Название секции')),
                ('gender', models.CharField(blank=True, max_length=7, verbose_name='Пол детей')),
                ('aviable', models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MinLengthValidator(1, message='Минимум 1 символ'), django.core.validators.MaxLengthValidator(3, message='Максимум 3 символа')], verbose_name='Наличие свободных мест')),
                ('price', models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MinLengthValidator(1, message='Минимум 1 символ'), django.core.validators.MaxLengthValidator(6, message='Максимум 6 символов')], verbose_name='Стоимость посещения секции в месяц в рублях')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.address', verbose_name='Адрес секции')),
                ('age_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.agegroup', verbose_name='Возрастная группа')),
                ('sport_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.sportorganization', verbose_name='Спортивная школа')),
            ],
            options={
                'verbose_name': 'Секция',
                'verbose_name_plural': 'Секции',
                'ordering': ('sport_organization', 'title'),
            },
        ),
        migrations.CreateModel(
            name='SportType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название вида спорта')),
            ],
            options={
                'verbose_name': 'Вид спорта',
                'verbose_name_plural': 'Виды спорта',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Фамилия Имя Отчество')),
                ('info', models.TextField(blank=True, max_length=10000, verbose_name='Информация о тренере')),
                ('photo', models.ImageField(blank=True, upload_to='img/trainers', verbose_name='Фотография тренера')),
            ],
            options={
                'verbose_name': 'Тренер',
                'verbose_name_plural': 'Тренера',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Shedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_from', models.TimeField(verbose_name='Время начала')),
                ('time_until', models.TimeField(verbose_name='Время окончания')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.dayofweek', verbose_name='День недели')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.section', verbose_name='Секция')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='SectionTrainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.section', verbose_name='Секция')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.trainer', verbose_name='Тренер')),
            ],
            options={
                'verbose_name': 'Секция и тренер',
                'verbose_name_plural': 'Секции и тренера',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='section',
            name='sport_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.sporttype', verbose_name='Вид спорта'),
        ),
        migrations.CreateModel(
            name='PhotoOfSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='img/sections', verbose_name='Фотография секции')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.section', verbose_name='Секция')),
            ],
            options={
                'verbose_name': 'Фотография секции',
                'verbose_name_plural': 'Фотографии секции',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='PhoneOfSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.phonenumber', verbose_name='Номер телефона')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sections.section', verbose_name='Секция спортивной школы')),
            ],
            options={
                'verbose_name': 'Телефон секции',
                'verbose_name_plural': 'Телефоны секции',
            },
        ),
    ]
