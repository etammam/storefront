# Generated by Django 4.0.3 on 2022-03-07 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.CharField(max_length=11, null=True),
        ),
    ]