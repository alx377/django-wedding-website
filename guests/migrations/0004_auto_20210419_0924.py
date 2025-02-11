# Generated by Django 3.1.7 on 2021-04-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0003_remove_party_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='invitation_sent',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='whatsapp_inviter',
            field=models.CharField(blank=True, choices=[('aleksi', 'aleksi'), ('marika', 'marika')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='diet',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
