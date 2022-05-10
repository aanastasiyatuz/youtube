# Generated by Django 4.0.4 on 2022-05-04 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_alter_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeeLater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='see_later', to='app.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='see_later', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
