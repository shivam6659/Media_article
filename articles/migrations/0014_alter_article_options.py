# Generated by Django 5.1.4 on 2024-12-14 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_alter_article_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'permissions': [('can_submit_article', 'Can submit article'), ('can_review_article', 'Can review article'), ('can_publish_article', 'Can publish article')]},
        ),
    ]
