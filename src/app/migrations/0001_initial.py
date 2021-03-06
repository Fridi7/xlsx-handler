# Generated by Django 3.2.5 on 2021-07-25 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='XlsxFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('file', models.FileField(null=True, upload_to='documents/')),
                ('task_id', models.UUIDField(null=True)),
            ],
        ),
    ]
