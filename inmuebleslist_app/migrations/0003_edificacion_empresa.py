# Generated by Django 5.0.6 on 2024-05-23 01:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebleslist_app', '0002_edificacion_empresa_delete_inmueble'),
    ]

    operations = [
        migrations.AddField(
            model_name='edificacion',
            name='empresa',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='edificacion', to='inmuebleslist_app.empresa'),
            preserve_default=False,
        ),
    ]