# Generated by Django 3.2.3 on 2023-11-01 12:48

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport_organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('title', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Название организации')),
                ('logo', models.ImageField(upload_to='img/organizations', verbose_name='Логотип организации')),
                ('email', models.EmailField(max_length=320, unique=True, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Адрес электронной почты')),
                ('site', models.CharField(blank=True, max_length=255, verbose_name='Сайт или страничка в VK')),
                ('description', models.TextField(max_length=20000, verbose_name='Описание организации')),
                ('login', models.CharField(max_length=60, unique=True, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Логин')),
                ('password', models.CharField(max_length=16, validators=[django.core.validators.MinLengthValidator(8, message='Минимум 8 символов')], verbose_name='Пароль')),
            ],
            options={
                'verbose_name': 'Спортивная школа',
                'verbose_name_plural': 'Спортивные школы',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField(validators=[django.core.validators.MinLengthValidator(6, message='Минимум 6 символов'), django.core.validators.MaxLengthValidator(6, message='Максимум 6 символов')], verbose_name='Индекс')),
                ('city', models.CharField(max_length=25, validators=[django.core.validators.MinLengthValidator(2, message='Минимум 2 символа')], verbose_name='Город')),
                ('metro', models.CharField(blank=True, max_length=65, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Метро')),
                ('district', models.CharField(max_length=65, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Район')),
                ('street', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Улица')),
                ('house', models.PositiveIntegerField(validators=[django.core.validators.MinLengthValidator(1, message='Минимум 1 символ'), django.core.validators.MaxLengthValidator(65, message='Максимум 65 символов')], verbose_name='Дом')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
                'ordering': ('city', 'street', 'house'),
            },
        ),
        migrations.CreateModel(
            name='Phone_number',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=18, validators=[django.core.validators.MinLengthValidator(18, message='Минимум 18 символов')], verbose_name='Телефон')),
                ('comment', models.CharField(blank=True, max_length=30, verbose_name='Комментарий к номеру телефона')),
            ],
        ),
        migrations.CreateModel(
            name='Rewiev',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=255, verbose_name='Текст отзыва')),
                ('date_and_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время оставления отзыва')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinLengthValidator(1, message='Минимум 1 символ'), django.core.validators.MaxLengthValidator(1, message='Максимум 1 символ'), django.core.validators.MinValueValidator(1, message='Минимумальное значение 1'), django.core.validators.MaxValueValidator(5, message='Максимальноезначение 5')], verbose_name='Рейтинг')),
                ('sport_school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Спортивная школа')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Phone_of_organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.phone_number', verbose_name='Телефон')),
                ('sport_school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Спортивная школа')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов')], verbose_name='Фамилия Имя Отчество')),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MinLengthValidator(1, message='Минимум 1 символ'), django.core.validators.MaxLengthValidator(2, message='Максимум 2 символа')], verbose_name='Возраст ребенка')),
                ('gender', models.CharField(max_length=7, verbose_name='Пол ребенка')),
                ('phone', models.CharField(max_length=18, validators=[django.core.validators.MinLengthValidator(18, message='Минимум 18 символов')], verbose_name='Номер телефона для связи')),
                ('comment', models.CharField(blank=True, max_length=255, verbose_name='Комментраий к заявке')),
                ('sport_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Спортивная школа')),
            ],
        ),
        migrations.AddField(
            model_name='sport_organization',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.address', verbose_name='Адрес спортивной школы'),
        ),
        migrations.AddField(
            model_name='sport_organization',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='sport_organization',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='sport_organization',
            constraint=models.UniqueConstraint(fields=('email', 'login'), name='unique_email_login'),
        ),
    ]
