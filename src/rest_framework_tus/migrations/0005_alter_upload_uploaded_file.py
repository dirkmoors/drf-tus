# Generated by Django 4.2.2 on 2023-07-04 06:56

from django.db import migrations, models

import rest_framework_tus.models


class Migration(migrations.Migration):
    dependencies = [
        ("rest_framework_tus", "0004_alter_upload_id_alter_upload_upload_metadata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="upload",
            name="uploaded_file",
            field=models.FileField(
                blank=True,
                max_length=255,
                null=True,
                upload_to=rest_framework_tus.models.custom_upload_path,
            ),
        ),
    ]