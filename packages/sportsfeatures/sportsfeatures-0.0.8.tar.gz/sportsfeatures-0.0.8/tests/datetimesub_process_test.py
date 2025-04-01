"""Tests for the datetimesub process function."""
import datetime
import os
import tempfile
import unittest

import pandas as pd

from sportsfeatures.datetimesub_process import datetimesub_process


class TestDatetimesubProcess(unittest.TestCase):

    def test_datetimesub_process(self):
        print("AND HERE")
        dt_column = "dt"
        df = pd.DataFrame(data={
            dt_column: [datetime.datetime(2022, 1, 1), datetime.datetime(2022, 1, 2), datetime.datetime(2022, 1, 3)],
            "dt_other": [datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.utc), datetime.datetime(2022, 1, 2, tzinfo=datetime.timezone.utc), datetime.datetime(2022, 1, 3, tzinfo=datetime.timezone.utc)],
        })
        datetimesub_process(df, dt_column)
