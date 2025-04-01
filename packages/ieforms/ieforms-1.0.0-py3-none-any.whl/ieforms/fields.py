# ieforms/fields.py
from django.forms.fields import RegexField
from django.utils.translation import gettext_lazy as _

class EircodeField(RegexField):
    """
    A Django form field for validating Irish Eircodes (Postcodes).

    - The Eircode is uppercased and formatted correctly.
    - It follows the official Eircode format.
    """

    default_error_messages = {"invalid": _("Enter a valid Eircode.")}

    def __init__(self, **kwargs):
        kwargs.setdefault('strip', True)
        super().__init__("^(D6W|[AC-FHKNPRTV-Y][0-9]{2})([AC-FHKNPRTV-Y0-9]{4})$", **kwargs)

    def to_python(self, value):
        """Convert input into uppercase without spaces."""
        value = super().to_python(value)
        if value in self.empty_values:
            return value
        return value.upper().replace(" ", "")

    def prepare_value(self, value):
        """Format the Eircode with a space in display."""
        value = self.to_python(value)
        if value in self.empty_values:
            return value
        return f'{value[:3]} {value[3:]}'
