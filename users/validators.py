from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError

MIN_AGE = 9
DOMAIN = 'rambler'


def AgeCheckValidator(value: date):
    difference = relativedelta(date.today(), value).years
    if difference < MIN_AGE:
        raise ValidationError(
            "%(value) is too small",
            params={"value", value}
        )


def CheckEmail(value: str):
    if DOMAIN in value:
        raise ValidationError(
          "%(value) is not correct",
          params={"value", value}
        )
