# Generated by Django 4.2 on 2023-12-29 17:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("catalogue", "0002_producttype_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="producttype",
            name="creat_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="producttype",
            name="modified_time",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
