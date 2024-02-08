#!/usr/bin/python3
import os
import django
import sqlite3
import pandas as pd

# set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'councilor_rater.settings')
django.setup()

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from crep.models import Province, Municipality, Ward, Councilor


# class Province(models.Model):
#     """
#     Represents a geographic province.
#     """
#     name = models.CharField(max_length=100)


# class Municipality(models.Model):
#     """
#     Represents a municipal subdivision within a province.
#     """
#     name = models.CharField(max_length=100)
#     province = models.ForeignKey(Province, on_delete=models.CASCADE)


# class Ward(models.Model):
#     """
#     Represents a ward or electoral division within a municipality.
#     """
#     ward_number = models.IntegerField(unique=True)
#     municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='wards')


# class Councilor(models.Model):
#     """
#     Represents an elected councilor within a ward.
#     """
#     names = models.CharField(max_length=100, null=True, blank=True)
#     surname = models.CharField(max_length=100, null=True, blank=True)
#     ward = models.OneToOneField(Ward,  on_delete=models.CASCADE)
#     affiliation = models.CharField(max_length=100, null=True, blank=True)


# class Services(models.Model):
#     """
#     Represents services provided within a municipality.
#     """
#     service_name = models.CharField(max_length=200)

    
# class Rating(models.Model):
#     """
#     Represents user ratings for councilors and services.
#     """
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     councilor = models.ForeignKey(Councilor, on_delete=models.CASCADE)
#     service = models.ForeignKey(Services, on_delete=models.CASCADE)
#     section_or_area = models.CharField(max_length=50)
#     quarter = models.IntegerField()
#     year = models.IntegerField()
#     feedback = models.TextField(blank=True, null=True)

# Read the Excel file
excel_file = './app_data.csv'
df = pd.read_csv(excel_file, encoding='latin1')

print(df.head())

# Connect to the SQLite database
db_file = './db.sqlite3'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS province_province (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS municipality_municipality (
        id INTEGER PRIMARY KEY,
        name TEXT,
        province_id INTEGER REFERENCES province_province(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ward_ward (
        id INTEGER PRIMARY KEY,
        ward_number INTEGER UNIQUE,
        municipality_id INTEGER REFERENCES municipality_municipality(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS councilor_councilor (
        id INTEGER PRIMARY KEY,
        names TEXT,
        surnames TEXT,
        ward_id INTEGER REFERENCES ward_ward(id),
        affiliation TEXT
    )
''')

# Insert data into tables
for _, row in df.iterrows():
    # Get or create province
    province, _ = Province.objects.get_or_create(name=row['Province'])
    
    # Get or create municipality
    municipality, _ = Municipality.objects.get_or_create(name=row['Municipality'], province=province)
    
    # Get or create ward
    ward, _ = Ward.objects.get_or_create(ward_number=row['Ward No'], municipality=municipality)
    
    # Create councilor
    Councilor.objects.create(names=row['Name(s)'], surname=row['Surname'], ward=ward, affiliation=row['Affilliation'])

# Commit changes and close the connection
conn.commit()
conn.close()

print('Data inserted successfully!')

