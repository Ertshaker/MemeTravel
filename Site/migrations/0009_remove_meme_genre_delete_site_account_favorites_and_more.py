# Generated by Django 5.0.4 on 2024-05-22 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0008_merge_20240522_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meme',
            name='genre',
        ),
        migrations.DeleteModel(
            name='Site_account_favorites',
        ),
        migrations.AddField(
            model_name='meme',
            name='cultural_influence',
            field=models.TextField(default='Тогда почему ты мой писарь, а?'),
        ),
        migrations.AddField(
            model_name='meme',
            name='history',
            field=models.TextField(default='Тогда почему ты мой писарь, а?'),
        ),
        migrations.AddField(
            model_name='meme',
            name='meaning',
            field=models.TextField(default='Тогда почему ты мой писарь, а?'),
        ),
        migrations.AddField(
            model_name='meme',
            name='using_examples',
            field=models.TextField(default='Тогда почему ты мой писарь, а?'),
        ),
        migrations.AlterField(
            model_name='meme',
            name='description',
            field=models.TextField(default='Тогда почему ты мой писарь, а?'),
        ),
        migrations.DeleteModel(
            name='Genres',
        ),
    ]