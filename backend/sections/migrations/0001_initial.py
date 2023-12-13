# Generated by Django 4.2.7 on 2023-12-13 21:00

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
            name='DayOfWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='День недели')),
            ],
            options={
                'verbose_name': 'День недели',
                'verbose_name_plural': 'Дни недели',
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
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Название секции')),
                ('gender', models.CharField(blank=True, choices=[('Man', 'мальчик'), ('Woman', 'девочка')], max_length=7, verbose_name='Пол детей')),
                ('year_from', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(3, message='Минимальное значение 3'), django.core.validators.MaxValueValidator(18, message='Максимальное значение 18')], verbose_name='Нижняя граница возрастной группы')),
                ('year_until', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(3, message='Минимальное значение 3'), django.core.validators.MaxValueValidator(18, message='Максимальное значение 18')], verbose_name='Верхняя граница возрастной группы')),
                ('address', models.CharField(max_length=350, verbose_name='Адрес секции')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=12, null=True, verbose_name='Широта')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=12, null=True, verbose_name='Долгота')),
                ('aviable', models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MaxValueValidator(999, message='Максимальное значение 999')], verbose_name='Наличие свободных мест')),
                ('price', models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MaxValueValidator(99999, message='Максимальное значение 99999')], verbose_name='Стоимость посещения секции в месяц в рублях')),
                ('free_class', models.BooleanField(blank=True, default=False, verbose_name='Бесплатное пробное занятие')),
                ('schedule', models.ManyToManyField(to='sections.dayofweek', verbose_name='День недели')),
                ('sport_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.sportorganization', verbose_name='Спортивная школа')),
                ('sport_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sections.sporttype', verbose_name='Вид спорта')),
            ],
            options={
                'verbose_name': 'Секция',
                'verbose_name_plural': 'Секции',
                'ordering': ('sport_organization', 'title'),
            },
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
            },
        ),
    ]
