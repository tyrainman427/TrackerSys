# Generated by Django 3.0.4 on 2020-03-17 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_auto_20200317_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='current_status',
            field=models.CharField(choices=[('Assigned', 'Assigned'), ('Open', 'Open'), ('Pending', 'Pending'), ('Closed', 'Closed')], max_length=10),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Med', 'Medium'), ('High', 'High')], max_length=10),
        ),
    ]
