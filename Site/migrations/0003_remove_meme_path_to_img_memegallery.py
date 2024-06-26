# Generated by Django 5.0.4 on 2024-05-07 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0002_remove_userpermission_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meme',
            name='path_to_img',
        ),
        migrations.CreateModel(
            name='MemeGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='memes/')),
                ('meme_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Site.meme')),
            ],
            options={
                'unique_together': {('meme_id', 'image')},
            },
        ),
    ]
