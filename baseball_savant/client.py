import collections
import io
import os
import pandas as pd
import requests


from .helpers import parse_dataframe
from .utils import get_request_date

REQ_DATE = get_request_date()
ROOT_URL = "https://baseballsavant.mlb.com"
SMALL_REQ = "/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7CPO%7CS%7C=&hfSea=&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt={start_dt}&game_date_lt={end_dt}&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_abs=0&type=details&"


class BaseballSavantException(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class BaseballSavant:
    def __init__(self):
        """Initialize the client"""
        self._date = REQ_DATE
        self._url = ROOT_URL + SMALL_REQ.format(start_dt=self._date, end_dt=self._date)

    # Perform initial request
    def get_data(self):
        """Perform the initial request, attempt to read into a DF (.CSV source),
        Pass the dataframe through the helper function
        Some exception handling, returns dataframe
        """
        self._content = requests.get(self._url, timeout=None).content.decode("utf-8")
        self._data = pd.read_csv(io.StringIO(self._content))
        self._data_cleaned = parse_dataframe(self._data)
        if self._data_cleaned is not None and not self._data_cleaned.empty:
            if "error" in self._data_cleaned.columns:
                raise BaseballSavantException(self._data_cleaned["error"].values[0])
            self._data_cleaned = self._data_cleaned.sort_values(
                ["game_date", "game_pk", "at_bat_number", "pitch_number"],
                ascending=False,
            )
        return self._data_cleaned
