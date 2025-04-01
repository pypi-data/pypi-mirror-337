# tests/test_fields.py
from ieforms.fields import EircodeField
from django.core.exceptions import ValidationError

def test_valid_eircode():
    field = EircodeField()
    assert field.clean("D02X285") == "D02X285"
    assert field.clean("D02 X285") == "D02X285"

def test_invalid_eircode():
    field = EircodeField()
    try:
        field.clean("INVALID")
    except ValidationError:
        assert True
    else:
        assert False
