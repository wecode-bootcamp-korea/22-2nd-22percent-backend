# Generated by Django 3.2.5 on 2021-07-21 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('deals', '0001_initial'),
        ('investments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdeal',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user'),
        ),
        migrations.AddField(
            model_name='debtorpayback',
            name='deal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='deals.deal'),
        ),
        migrations.AddField(
            model_name='debtorpayback',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='investments.paybackstate'),
        ),
        migrations.AddConstraint(
            model_name='userdeal',
            constraint=models.UniqueConstraint(fields=('user', 'deal'), name='unique_user_deal'),
        ),
    ]
