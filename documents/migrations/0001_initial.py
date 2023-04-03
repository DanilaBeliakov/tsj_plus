# Generated by Django 4.1.7 on 2023-04-02 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='documents',
            fields=[
                ('document_id', models.IntegerField(primary_key=True, serialize=False)),
                ('document_text', models.TextField()),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=20)),
                ('house_id', models.IntegerField()),
                ('document_date', models.DateField()),
            ],
        ),
    ]
