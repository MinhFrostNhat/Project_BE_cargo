# Generated by Django 3.1.5 on 2021-09-16 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project_cargo', '0004_auto_20210818_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_inf',
            name='image',
            field=models.ImageField(default='x.jpg', upload_to='Img_media'),
        ),
    ]
