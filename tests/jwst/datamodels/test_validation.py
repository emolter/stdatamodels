from datetime import datetime

import numpy as np
import pytest
from asdf.exceptions import ValidationError
from astropy import time

from stdatamodels.jwst.datamodels import JwstDataModel, RampModel


def test_strict_validation_enum():
    with JwstDataModel(strict_validation=True) as dm:
        assert dm.meta.instrument.name is None
        with pytest.raises(ValidationError):
            # FOO is not in the allowed enumerated values
            dm.meta.instrument.name = "FOO"


def test_strict_validation_type():
    with JwstDataModel(strict_validation=True) as dm:
        with pytest.raises(ValidationError):
            # Schema requires a float
            dm.meta.target.ra = "FOO"


def test_strict_validation_date():
    with JwstDataModel(strict_validation=True) as dm:
        time_obj = time.Time(dm.meta.date)
        assert isinstance(time_obj, time.Time)
        date_obj = datetime.strptime(dm.meta.date, "%Y-%m-%dT%H:%M:%S.%f")
        assert isinstance(date_obj, datetime)


def test_array_shape_validation():
    # use RampModel because need a primary array, and JwstDataModel generic doesn't have one
    with RampModel((2, 3, 4, 5), strict_validation=True, validate_arrays=True) as dm:
        assert dm.shape == (2, 3, 4, 5)

        # Setting to wrong last two dimensions raises ValidationError
        with pytest.raises(ValidationError):
            dm.err = np.zeros((2, 3, 4, 6))
        with pytest.raises(ValidationError):
            dm.err = np.zeros((2, 3, 5, 5))
        with pytest.raises(ValidationError):
            dm.err = np.zeros((5))

        # but other dimensions are not checked
        dm.err = np.zeros((3, 4, 4, 5))
        dm.err = np.zeros((4, 5))
        dm.err = np.zeros((2, 4, 5))
