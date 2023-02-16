# Generated by Django 4.1.6 on 2023-02-15 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='accounts',
        ),
        migrations.CreateModel(
            name='Account_Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userType', models.CharField(choices=[('1', 'Sender'), ('2', 'Receiver')], default='1', max_length=1)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.account')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.transaction')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='accounts',
            field=models.ManyToManyField(to='bank.account'),
        ),
    ]
