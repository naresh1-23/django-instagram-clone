# Generated by Django 4.2.6 on 2023-10-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_posted_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='posted_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
