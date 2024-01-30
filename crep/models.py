from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ward(models.Model):
    ward_number = models.IntegerField(unique=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ward {self.ward_number} - {self.municipality}"


class Councilor(models.Model):
    names = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    ward = models.OneToOneField(Ward,  on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=100, null=True, blank=True)

    # Determine the number of ratings made for each councilor
    def no_of_ratings(self):
        ratings = Rating.objects.filter(councilor=self)
        return len(ratings)

    # Determine average ratings for each councilor
    def avg_ratings(self):
        total = 0
        ratings = Rating.objects.filter(councilor=self)
        for rating in ratings:
            total += rating.stars
        if len(ratings) > 0:
            return total / len(ratings)
        else:
            return 0

    def __str__(self):
        return f"{self.names} {self.surname}, Ward {self.ward}"


class Services(models.Model):
    service_name = models.CharField(max_length=200)

    def __str__(self):
        return self.service_name
    
