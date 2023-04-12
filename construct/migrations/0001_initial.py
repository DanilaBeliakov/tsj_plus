# Generated by Django 4.1.7 on 2023-04-11 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='notification',
            fields=[
                ('notification_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type_of_voting', models.CharField(max_length=15)),
                ('type_of_plans', models.CharField(default='', max_length=15)),
                ('place_of_meeting', models.CharField(max_length=100)),
                ('date_of_start', models.CharField(default='', max_length=30)),
                ('date_of_end', models.CharField(default='', max_length=30)),
                ('time_of_start', models.CharField(default='', max_length=30)),
                ('time_of_end', models.CharField(default='', max_length=30)),
                ('notification_file', models.FileField(blank=True, null=True, upload_to='files/notifications/')),
            ],
        ),
        migrations.CreateModel(
            name='statement',
            fields=[
                ('statement_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('statement_file', models.FileField(blank=True, null=True, upload_to='files/statements/')),
            ],
        ),
        migrations.CreateModel(
            name='temp_elections',
            fields=[
                ('temp_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('house_id', models.IntegerField(default=0)),
                ('num_in_meeting', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='meetings',
            fields=[
                ('meeting_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('stage', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField(default='01-01-2000')),
                ('house_id', models.IntegerField()),
                ('notification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='construct.notification')),
                ('statement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='construct.statement')),
            ],
        ),
    ]
