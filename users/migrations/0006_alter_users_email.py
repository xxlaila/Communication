# Generated by Django 3.2.7 on 2021-09-14 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210912_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='邮箱'),
        ),
    ]
