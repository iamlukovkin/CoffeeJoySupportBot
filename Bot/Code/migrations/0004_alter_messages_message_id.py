# Generated by Django 4.2.4 on 2023-08-25 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Code', '0003_remove_messages_id_messages_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='message_id',
            field=models.IntegerField(blank=True, default=0, primary_key=True, serialize=False),
        ),
    ]
