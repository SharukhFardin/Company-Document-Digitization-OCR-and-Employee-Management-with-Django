# Generated by Django 3.2 on 2021-05-17 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0009_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ManyToManyField(to='admin_page.Plan_User'),
        ),
    ]