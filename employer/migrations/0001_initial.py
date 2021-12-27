# Generated by Django 4.0 on 2021-12-21 09:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Age')),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], default=1, verbose_name='Gender')),
                ('phone', models.CharField(blank=True, max_length=25, null=True, verbose_name='Phone')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer', to='auth.user')),
            ],
        ),
    ]
