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


class Councilor(models.Model):
    names = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    municipality = models.CharField(max_length=100, null=True, blank=True)
    ward_number = models.IntegerField()
    affiliation = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.names} {self.surname}, of {self.municipality} Ward {self.ward_number}"


class Services(models.Model):
    service_name = models.CharField(max_length=200)

    def __str__(self):
        return self.service_name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    councilor = models.ForeignKey(Councilor, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    section_or_area = models.CharField(max_length=50)
    quarter = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return (f"{self.user} of ({self.section_or_area}) rates {self.councilor} for {self.service} "
                f"with {self.stars} stars")

    class Meta:
        #  Ensure that a user can only rate a councilor of their ward only once a quarter
        unique_together = ['user', 'councilor', 'quarter', 'year']

    def save(self, *args, **kwargs):
        #  Set the current quarter and year if not provided
        if not self.quarter or not self.year:
            now = timezone.now()
            self.quarter = (now.month - 1) // 3 + 1
            self.year = now.year
        super().save(*args, **kwargs)
