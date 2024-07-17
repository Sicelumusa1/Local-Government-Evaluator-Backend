#!/usr/bin/python3

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Avg

# Create your models here.


class Province(models.Model):
    """
    Represents a geographic province.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    """
    Represents a municipal subdivision within a province.
    """
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ward(models.Model):
    """
    Represents a ward or electoral division within a municipality.
    """
    ward_number = models.IntegerField(unique=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='wards')

    def __str__(self):
        return f"Ward {self.ward_number} - {self.municipality}"


class Councilor(models.Model):
    """
    Represents an elected councilor within a ward.
    """
    names = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    ward = models.OneToOneField(Ward,  on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=100, null=True, blank=True)

    # Determine the number of ratings made for each councilor
    def no_of_ratings(self):
        """
        Determines the number of rating made for each councilor.
        """
        return Rating.objects.filter(councilor=self).values('user').distinct().count()

    # Determine average ratings for each councilor
    def avg_ratings(self):
        """
        Determines the average ratings for each councilor.
        """
        return Rating.objects.filter(councilor=self).aggregate(avg_rating=Avg('stars'))['avg_rating'] or 0

    def __str__(self):
        return f"{self.names} {self.surname}, Ward {self.ward}"


class Services(models.Model):
    """
    Represents services provided within a municipality.
    """
    service_name = models.CharField(max_length=200)

    def __str__(self):
        return self.service_name
    
class Rating(models.Model):
    """
    Represents user ratings for councilors and services.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    councilor = models.ForeignKey(Councilor, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    section_or_area = models.CharField(max_length=50)
    quarter = models.IntegerField()
    year = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"{self.user} of ({self.section_or_area}) rates {self.councilor} for {self.service} "
                f"with {self.stars} stars")

    class Meta:
        #  Ensure that a user can only rate a councilor of their ward only once a quarter
        unique_together = ['user', 'councilor', 'service', 'quarter', 'year']

    def save(self, *args, **kwargs):
        #  Set the current quarter and year if not provided
        if not self.quarter or not self.year:
            now = timezone.now()
            self.quarter = (now.month - 1) // 3 + 1
            self.year = now.year
        super().save(*args, **kwargs)


class Perspective(models.Model):
    """
    Represents the perpectives of the residents with regards to the councilors perfomance
    """
    tittle = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Petition(models.Model):
    """
    Represents the pertition set in motion by residents in case they are dissatisfied 
    with the leadership of their councilor
    """
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    signatures = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='petitions_signed', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def sign_petition(self, user):
        """
        Adds a user's signature to the petition.
        """
        self.signatures.add(user)

    def remove_signature(self, user):
        """
        Removes a user's signature from the petition.
        """
        self.signatures.remove(user)
    
    def total_signatures(self):
        """
        Returns the total number of signatures on the petition.
        """
        return self.signatures.count()