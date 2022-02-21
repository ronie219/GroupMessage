# Generated by Django 4.0.2 on 2022-02-20 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='id',
            field=models.UUIDField(default=uuid.UUID('36d2b30d-b8ef-48f2-bad0-a704f479a178'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('0a3b7a78-7eed-449f-a30f-cd20a5febfc4'), primary_key=True, serialize=False, unique=True)),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_name', to='chat.groups')),
                ('user_id', models.ManyToManyField(related_name='group_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
