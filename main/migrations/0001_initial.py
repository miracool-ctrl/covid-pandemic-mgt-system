# Generated by Django 3.1.6 on 2024-08-31 04:36

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bed_number', models.CharField(max_length=10)),
                ('occupied', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone_num', models.CharField(max_length=15)),
                ('patient_relative_name', models.CharField(max_length=50, null=True)),
                ('patient_relative_contact', models.CharField(max_length=15, null=True)),
                ('address', models.TextField()),
                ('symptoms', multiselectfield.db.fields.MultiSelectField(choices=[('Fever', 'Fever'), ('Dry cough', 'Dry cough'), ('Tiredness', 'Tiredness'), ('Aches and pains', 'Aches and pains'), ('Sore throat', 'Sore throat'), ('Diarrhoea', 'Diarrhoea'), ('Loss of taste or smell', 'Loss of taste or smell'), ('Difficulty in breathing or shortness of breath', 'Difficulty in breathing or shortness of breath'), ('Chest pain or pressure', 'Chest pain or pressure'), ('Loss of speech or movement', 'Loss of speech or movement')], max_length=183, null=True)),
                ('prior_ailments', models.TextField()),
                ('dob', models.DateField(null=True)),
                ('doctors_notes', models.TextField(blank=True, null=True)),
                ('doctors_visiting_time', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(max_length=50)),
                ('bed_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bed')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.doctor')),
            ],
        ),
    ]
