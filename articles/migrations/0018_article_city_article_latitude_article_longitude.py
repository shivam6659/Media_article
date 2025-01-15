# Generated by Django 4.2.16 on 2025-01-02 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0017_article_author_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
