# Generated by Django 3.2 on 2021-05-01 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_comment_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='room_desc',
            new_name='comment',
        ),
    ]
