# Generated by Django 4.2.4 on 2023-08-25 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Code', '0002_users_answered_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='id',
        ),
        migrations.AddField(
            model_name='messages',
            name='message_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]