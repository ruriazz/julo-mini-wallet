# Generated by Django 5.0.1 on 2024-02-01 06:40

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('SUCCESS', 'success'), ('FAILED', 'failed')], default=None, max_length=10, null=True)),
                ('transacted_at', models.DateTimeField(auto_now_add=True)),
                ('transaction_type', models.CharField(choices=[('DEPOSIT', 'deposit'), ('WITHDRAWAL', 'withdrawal')], max_length=10)),
                ('amount', models.PositiveBigIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('reference_id', models.UUIDField()),
                ('system_notes', models.TextField(blank=True, default=None, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('wallet', models.ForeignKey(db_column='wallet_id', on_delete=django.db.models.deletion.CASCADE, to='wallet.wallet')),
            ],
            options={
                'db_table': 'wallet_transaction',
            },
        ),
    ]
