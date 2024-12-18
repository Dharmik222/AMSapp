# Generated by Django 4.2.5 on 2024-11-18 11:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alumnis_delete_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumni',
            name='addr',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='price',
        ),
        migrations.AddField(
            model_name='alumni',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='alumni',
            name='date_of_death',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumni',
            name='family_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumni',
            name='full_name',
            field=models.CharField(default='Full Name', max_length=255),
        ),
        migrations.AddField(
            model_name='alumni',
            name='funeral_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumni',
            name='notable_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alumni',
            name='obituary_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='alumni',
            name='university_affiliation',
            field=models.TextField(default='Unknown University'),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
