# Generated by Django 5.1.1 on 2024-09-21 16:24

import blog.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.upload_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.upload_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.user'),
        ),
    ]