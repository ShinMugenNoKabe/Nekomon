# Generated by Django 4.0.4 on 2022-05-23 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nekomon', '0007_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='in_response_to',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='nekomon.post'),
            preserve_default=False,
        ),
    ]