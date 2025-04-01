# ieforms/widgets.py
from django.forms.widgets import Select
from .constants import IE_COUNTY_CHOICES

class IECountySelect(Select):
    """A Select widget for Irish Counties."""
    def __init__(self, attrs=None):
        super().__init__(attrs, choices=IE_COUNTY_CHOICES)
