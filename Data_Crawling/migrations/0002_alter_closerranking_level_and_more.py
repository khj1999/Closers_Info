# Generated by Django 4.1 on 2024-05-16 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data_Crawling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closerranking',
            name='level',
            field=models.CharField(max_length=50, verbose_name='레벨'),
        ),
        migrations.AlterField(
            model_name='closerranking',
            name='ranking',
            field=models.CharField(max_length=50, verbose_name='랭킹'),
        ),
    ]
