# Generated by Django 4.2.3 on 2023-07-13 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_news_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='2023-07-13')),
            ],
        ),
        migrations.CreateModel(
            name='WordCloud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string', models.TextField()),
                ('count', models.IntegerField()),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='home.defaultdate')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='date',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='news', to='home.defaultdate'),
            preserve_default=False,
        ),
    ]
