# Generated by Django 3.2.3 on 2023-11-11 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agegroup',
            options={'verbose_name': 'Возрастная группа', 'verbose_name_plural': 'Возрастные группы'},
        ),
        migrations.AlterModelOptions(
            name='photoofsection',
            options={'verbose_name': 'Фотография секции', 'verbose_name_plural': 'Фотографии секции'},
        ),
        migrations.AlterModelOptions(
            name='shedule',
            options={'verbose_name': 'Расписание', 'verbose_name_plural': 'Расписания'},
        ),
        migrations.AlterModelOptions(
            name='sporttype',
            options={'verbose_name': 'Вид спорта', 'verbose_name_plural': 'Виды спорта'},
        ),
        migrations.AlterModelOptions(
            name='trainer',
            options={'verbose_name': 'Тренер', 'verbose_name_plural': 'Тренера'},
        ),
    ]
