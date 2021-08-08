import pandas as pd
import re

date_formats = [
    # Standard statcast format
    (re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$'), '%Y-%m-%d'),

    # Just in case (https://github.com/jldbc/pybaseball/issues/104)
    (re.compile(r'^\d{4}-\d{1,2}-\d{1,2}T\d{2}:\d{2}:\d{2}.\d{1,6}Z$'), '%Y-%m-%dT%H:%M:%S.%fZ'),
]

def parse_dataframe(data):
    data_copy = data.copy()

    string_columns = [
        dtype_tuple[0] for dtype_tuple in data_copy.dtypes.items() if str(dtype_tuple[1]) in ["object","string"]
    ]

    for column in string_columns:
        # Only check the first value of the column and test that;
        # this is faster than blindly trying to convert entire columns
        first_value_index = data_copy[column].first_valid_index()
        if first_value_index is None:
            # All nulls
            continue
        first_value = data_copy[column].loc[first_value_index]

        if str(first_value).endswith('%') or column.endswith('%'):
            data_copy[column] = data_copy[column].astype(str).str.replace("%", "").astype(float) / 100.0
        else:
            # Doing it this way as just applying pd.to_datetime on
            # the whole dataframe just tries to gobble up ints/floats as timestamps
            for date_regex, date_format in date_formats:
                if isinstance(first_value, str) and date_regex.match(first_value):
                    data_copy[column] = data_copy[column].apply(pd.to_datetime, errors='ignore', format=date_format)
                    data_copy[column] = data_copy[column].convert_dtypes(convert_string=False)
                    break

    return data_copy




