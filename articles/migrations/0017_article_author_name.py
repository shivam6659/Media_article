# Generated by Django 4.2.16 on 2024-12-16 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_article_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author_name',
            field=models.TextField(max_length=50, null=True),
        ),
    ]
