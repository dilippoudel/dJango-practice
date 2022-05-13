# Generated by Django 4.0.4 on 2022-05-11 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_author_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter your Full name', max_length=50)),
                ('email', models.EmailField(help_text='Enter your valid Email Address', max_length=254)),
                ('message', models.CharField(max_length=500)),
                ('phone', models.CharField(help_text='Enter Your contact details', max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.book'),
        ),
    ]
