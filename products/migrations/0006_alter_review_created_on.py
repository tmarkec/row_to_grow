# Generated by Django 3.2 on 2023-05-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_review_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
