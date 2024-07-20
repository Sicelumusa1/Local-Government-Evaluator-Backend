#!/usr/bin/python3

"""
Registers models with the Django admin interface for easy management and visualization.

This module registers the following models with the Django admin interface:
- Province: Represents a geogrphic province.
- Municipulity: Represents a municipal subdivision within a province.
- Ward: Represents a ward or electoral division within a municipality.
- Councilor: Represents an elected councilor within a ward.
- Services: Represents services provided within a municipality.
- Rating: Represents ratings associated with services provided.
"""

from django.contrib import admin
from .models import Province, Municipality, Ward, Councilor, Services, Rating, Perspective, Petition


admin.site.register(Province)
admin.site.register(Municipality)
admin.site.register(Ward)
admin.site.register(Councilor)
admin.site.register(Services)
admin.site.register(Rating)
admin.site.register(Perspective)
admin.site.register(Petition)

