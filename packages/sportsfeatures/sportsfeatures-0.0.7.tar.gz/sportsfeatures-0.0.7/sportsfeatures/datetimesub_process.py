"""A processor for subbing any datetimes with the dt column."""

import logging

import pandas as pd
from feature_engine.datetime import DatetimeSubtraction


def datetimesub_process(df: pd.DataFrame, dt_column: str) -> pd.DataFrame:
    """Process date time subtractions."""
    columns = (
        df.drop(columns=[dt_column])
        .select_dtypes(
            include=["datetime", "datetime64", "datetime64[ns]", "datetimetz"]
        )
        .columns.values.tolist()
    )
    if columns:
        for column in columns:
            try:
                dts = DatetimeSubtraction(variables=[column], reference=[dt_column])  # type: ignore
                df = dts.fit_transform(df)
            except TypeError as exc:
                logging.warning(str(exc))
    return df
