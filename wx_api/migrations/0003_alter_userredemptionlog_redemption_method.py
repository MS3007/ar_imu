# Generated by Django 4.2.3 on 2023-09-24 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_api', '0002_userredemptionlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userredemptionlog',
            name='redemption_method',
            field=models.CharField(choices=[('1', '积分'), ('2', '游戏兑换'), ('3', '地点打卡兑换')], max_length=20, verbose_name='兑换方式'),
        ),
    ]
