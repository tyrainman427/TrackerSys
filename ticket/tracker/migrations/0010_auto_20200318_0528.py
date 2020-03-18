# Generated by Django 2.1.1 on 2020-03-18 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0009_ticket_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='is_admin',
        ),
        migrations.AddField(
            model_name='ticketuser',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Ticket'),
        ),
        migrations.AddField(
            model_name='ticketuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]