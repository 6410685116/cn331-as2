# Generated by Django 4.2.5 on 2023-09-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Register', '0005_remove_subject_students_subject_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='Subject', to='Register.student'),
        ),
    ]