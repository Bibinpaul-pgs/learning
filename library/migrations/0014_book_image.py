# Generated by Django 4.1.2 on 2022-11-09 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_alter_issuebook_issue_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
