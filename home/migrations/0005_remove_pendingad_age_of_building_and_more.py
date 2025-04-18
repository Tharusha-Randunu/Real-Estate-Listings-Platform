# Generated by Django 5.2 on 2025-04-13 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_pendingad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendingad',
            name='age_of_building',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='floors',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='furnishing_status',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='images',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='link',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='offer_type',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='parking',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='posted_by',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='property_features',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='property_type',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='seller_email',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='seller_name',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='seller_tel',
        ),
        migrations.RemoveField(
            model_name='pendingad',
            name='status',
        ),
        migrations.AddField(
            model_name='pendingad',
            name='property_image',
            field=models.ImageField(blank=True, null=True, upload_to='property_images/'),
        ),
        migrations.AlterField(
            model_name='pendingad',
            name='bathrooms',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='pendingad',
            name='bedrooms',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='pendingad',
            name='floor_area',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='pendingad',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pendingad',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pendingad',
            name='price_type',
            field=models.CharField(max_length=50),
        ),
    ]
