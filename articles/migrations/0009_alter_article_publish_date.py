# Generated by Django 4.2.3 on 2024-12-07 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publish_date',
            field=models.DateField(default='2024-01-01'),
        ),
    ]